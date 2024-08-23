from flask import Flask, request, jsonify
import base64
from googleapiclient.discovery import build

app = Flask(__name__)

# 處理來自 Pub/Sub 的推送消息
@app.route('/pubsub-push-endpoint', methods=['POST'])
def pubsub_push_handler():
    envelope = request.get_json()
    print('envelop:', envelope)
    
    # 解析 Pub/Sub 訊息
    if 'message' in envelope:
        pubsub_message = envelope['message']
        data = base64.urlsafe_b64decode(pubsub_message['data']).decode('utf-8')
        print(f"Received message: {data}")
        
        # 在這裡處理 Gmail 通知，例如檢查新郵件，下載附件等
        handle_gmail_notification(data)
    
    return jsonify(status="success"), 200

def handle_gmail_notification(data):
    # 解碼並解析推送的數據
    history_id = data.get('historyId')
    
    # 使用 Gmail API 查詢新郵件
    service = get_gmail_service()  # 認證獲取 Gmail API 服務
    history = service.users().history().list(userId='me', startHistoryId=history_id).execute()
    
    for message in history.get('messages', []):
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        
        for part in msg['payload']['parts']:
            if part['filename'] and 'attachmentId' in part['body']:
                attachment = service.users().messages().attachments().get(userId='me', messageId=message['id'], id=part['body']['attachmentId']).execute()
                data = base64.urlsafe_b64decode(attachment['data'])
                
                # 將附件保存並上傳到 Google Drive
                save_and_upload_attachment(part['filename'], data)

if __name__ == "__main__":
    app.run(port=8080, debug=True)