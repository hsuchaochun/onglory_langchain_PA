import pdfkit
import markdown2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import requests
import time
import config

def markdown_to_pdf(markdown_content, output_pdf, wkhtmltopdf_path=None, orientation='portrait'):
    # Convert markdown to HTML, ensuring it's UTF-8 encoded
    html_content = markdown2.markdown(markdown_content, extras=["tables"])

    # Set PDF options
    options = {
        'encoding': 'UTF-8',
        'orientation': orientation
    }

    # Make sure to specify the wkhtmltopdf path, if needed
    if wkhtmltopdf_path:
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
        pdfkit.from_string(html_content, output_pdf, configuration=config, options=options)
    else:
        pdfkit.from_string(html_content, output_pdf, options=options)
        
def send_email_with_attachment(smtp_server, port, sender_email, sender_password, recipient_email, cc_emails, subject, body, attachment_paths):
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['CC'] = ', '.join(cc_emails)  # Add CC recipients
    msg['Subject'] = subject

    # Attach the body text
    msg.attach(MIMEText(body, 'plain'))

    # Attach multiple files
    for attachment_path in attachment_paths:
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename= {attachment_path.split('/')[-1]}")
            msg.attach(part)

    # Collect all recipients (To + CC)
    recipients = [recipient_email] + cc_emails

    # Send the email via SMTP server
    with smtplib.SMTP_SSL(smtp_server, port) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipients, msg.as_string())
        
def generate_attachment_path(prefix):
    return f'./daily_summary/Onglory_{datetime.now().strftime("%Y%m%d")}_{prefix}.pdf'

def create_and_send_daily_summary():
    daily_summary_path = generate_attachment_path("daily_summary")
    trading_history_path = generate_attachment_path("trading_history")
    
    create_daily_summary_pdf(daily_summary_path)
    create_daily_trading_history_pdf(trading_history_path)
    
    attachment_paths = [daily_summary_path, trading_history_path]
    
    subject = "Onglory Crypto Daily Summary"
    body = "Please find the attached files."
    
    send_email_with_attachment(
        config.SMTP_SERVER, config.SSL_PORT, 
        config.SENDER_EMAIL, config.SENDER_EMAIL_PASSWORD, 
        config.RECIPIENT_EMAIL, config.CC_EMAILS, 
        subject, body, attachment_paths
    )
        
def create_daily_summary_pdf(attachment_path):
    trigger_response = requests.post(
        config.RELEVANCE_BASE_URL + "/agents/trigger", 
        headers=config.RELEVANCE_HEADERS, 
        json={
            "message":{
                "role":"user",
                "content":"市場彙整"
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
    markdown_to_pdf(send_msg, attachment_path, orientation='landscape')
    
    return

def create_daily_trading_history_pdf(attachment_path):
    body = {
        "params":{
            "objective": '''
Fetch the **latest 5 trades** for each of the **9 strategies** from the `'onglory_trading_history'` table. 
Sort the results by the column **'updateTime'** in **descending order** (most recent first). 
Only show the tables with the latest 5 trades for each strategy. 
For each strategy, display its trading history in **separate tables** with the following columns:

* **symbol**
* **price**
* **avgPrice**
* **origQty**
* **executedQty**
* **cumQuote**
* **cummulativeQuoteQty**
* **status**
* **side**
* **type**
* **origType**
* **time**
* **updateTime**

Ensure the trades are listed with the **most recent trade at the top** for each strategy's table.
The output should only display the strategy name followed by its table with 5 rows for each strategy.
'''
        },
        "project":config.RELEVANCE_PROJECT_ID
    }

    response = requests.post(
        config.RELEVANCE_BASE_URL + f"/studios/{config.RELEVANCE_TOOL_ID}/trigger_async", 
        headers=config.RELEVANCE_HEADERS, 
        json=body
    )

    # Extract the tools job id, so we can check its progress
    job = response.json()
    print(job)
    job_id = job['job_id']

    poll_url = config.RELEVANCE_BASE_URL + f"/studios/{config.RELEVANCE_TOOL_ID}/async_poll/{job_id}?ending_update_only=true"

    done = False
    # Every 3 seconds, check if the tool had finished by calling the poll endpoint
    while not done:
        poll_response = requests.get(poll_url, headers=config.RELEVANCE_HEADERS).json()
        if poll_response['type'] == "complete" or poll_response['type'] == 'failed':
            done = True
            break
        time.sleep(3)

    send_msg = poll_response['updates'][0]['output']['output']['llm_answer']
    print(send_msg)
    
    # export as pdf
    markdown_to_pdf(send_msg, attachment_path, orientation='landscape')
        
    return