import requests
import config
import time
import func
from datetime import datetime

current_time = datetime.now()
while 1:
    
    if current_time.hour==8 and current_time.minute==5:
        
        trigger_response = requests.post(
            config.RELEVANCE_BASE_URL + "/agents/trigger", 
            headers=config.RELEVANCE_HEADERS, 
            json={
                "message":{
                    "role":"user",
                    "content":"昨日市場彙整"
                },
            "agent_id":config.RELEVANCE_AGENT_ID
            }
        )

        job = trigger_response.json()

        print(job)

        studio_id = job["job_info"]["studio_id"]
        job_id = job["job_info"]["job_id"]

        done = False
        status = None

        while not done:
            response = requests.get(
                config.RELEVANCE_BASE_URL + f"/studios/{studio_id}/async_poll/{job_id}", 
                headers=config.RELEVANCE_HEADERS
            )

            status = response.json()

            for update in status['updates']:
                if update['type'] == "chain-success":
                    done = True

                if done:
                    break

            time.sleep(3)

        send_msg = status['updates'][0]['output']['output']['answer']
        print(send_msg)

        # export as pdf
        attachment_path = './daily_summary/Onglory_' + time.strftime("%Y%m%d") + "_daily_summary.pdf"
        func.markdown_to_pdf(send_msg, attachment_path)

        # send email
        subject = "Onglory Crypto Daily Summary"
        body = "Please find the attached file."
        func.send_email_with_attachment(config.SMTP_SERVER, config.SSL_PORT, config.SENDER_EMAIL, config.SENDER_EMAIL_PASSWORD, config.RECIPIENT_EMAIL, config.CC_EMAILS, subject, body, attachment_path)
        
        time.sleep(60)