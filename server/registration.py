from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import os

# 認證並獲取 Gmail API 服務
def authenticate_to_google(scopes):
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', scopes)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return build('gmail', 'v1', credentials=creds)

# 註冊 Gmail 推送通知
def setup_gmail_watch(service):
    request_body = {
        'labelIds': ['INBOX'],
        'topicName': 'projects/{your-project-id}/topics/gmail-notifications'
    }
    response = service.users().watch(userId='me', body=request_body).execute()
    print(f"Push notification setup: {response}")

def main():
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
    service = authenticate_to_google(SCOPES)
    setup_gmail_watch(service)

if __name__ == "__main__":
    main()