import os
import time
import pdfkit
import config
import smtplib
import requests
import markdown2
from datetime import datetime
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

def markdown_to_pdf(markdown_content, output_pdf, wkhtmltopdf_path=None, orientation='portrait'):
    html_content = markdown2.markdown(markdown_content, extras=["tables"])
    
    html_with_styles = f"""
    <html>
    <head>
        <style>
            table {{
                width: auto;
                table-layout: auto;
                border-collapse: collapse;
            }}
            th, td {{
                border: 1px solid black;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f2f2f2;
            }}
        </style>
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """

    options = {
        'encoding': 'UTF-8',
        'orientation': orientation
    }

    if wkhtmltopdf_path:
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
        pdfkit.from_string(html_with_styles, output_pdf, configuration=config, options=options)
    else:
        pdfkit.from_string(html_with_styles, output_pdf, options=options)

def send_email_with_attachment(smtp_server, port, sender_email, sender_password, recipient_email, cc_emails, subject, body, attachment_paths):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['CC'] = ', '.join(cc_emails)
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    for attachment_path in attachment_paths:
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename= {attachment_path.split('/')[-1]}")
            msg.attach(part)

    recipients = [recipient_email] + cc_emails

    with smtplib.SMTP_SSL(smtp_server, port) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipients, msg.as_string())

def generate_attachment_path(prefix):
    date_folder = datetime.now().strftime("%Y%m%d")
    os.makedirs(f'./daily_summary/{date_folder}', exist_ok=True)
    return f'./daily_summary/{date_folder}/Onglory_{date_folder}_{prefix}.pdf'

def create_pdf_report(attachment_path, agent_id, content):
    trigger_response = requests.post(
        config.RELEVANCE_BASE_URL + "/agents/trigger", 
        headers=config.RELEVANCE_HEADERS, 
        json={
            "message":{
                "role":"user",
                "content": content
            },
            "agent_id": agent_id
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

    markdown_to_pdf(send_msg, attachment_path, orientation='landscape')
    
    return

def create_investment_summary_pdf(attachment_path):
    create_pdf_report(attachment_path, config.RELEVANCE_INVESTMENT_SUMMARY_AGENT_ID, "Onglory投資彙整")

def create_financial_advice_pdf(attachment_path):
    create_pdf_report(attachment_path, config.RELEVANCE_FINANCIAL_ADVISE_AGENT_ID, "Daily market recommendations.")

def create_and_send_daily_summary():
    investment_summary_path = generate_attachment_path("investment_summary")
    financial_advice_path = generate_attachment_path("financial_advice")
    
    create_investment_summary_pdf(investment_summary_path)
    create_financial_advice_pdf(financial_advice_path)
    
    attachment_paths = [investment_summary_path, financial_advice_path]
    
    subject = "Onglory Crypto Daily Summary"
    body = "Please find the attached files."
    
    send_email_with_attachment(
        config.SMTP_SERVER, config.SSL_PORT, 
        config.SENDER_EMAIL, config.SENDER_EMAIL_PASSWORD, 
        config.RECIPIENT_EMAIL, config.CC_EMAILS, 
        subject, body, attachment_paths
    )
    
def news_categorize():
    body = {
        "params": {
            "number": 1, 
            "interval": "HOUR"
        },
        "project": config.RELEVANCE_PROJECT_ID
    }

    response = requests.post(
        config.RELEVANCE_BASE_URL + f"/studios/{config.RELEVANCE_NEWS_CATEGORIZE_TOOLS_ID}/trigger_async", 
        headers=config.RELEVANCE_HEADERS, 
        json=body
    )

    job = response.json()
    job_id = job['job_id']

    poll_url = config.RELEVANCE_BASE_URL + f"/studios/{config.RELEVANCE_NEWS_CATEGORIZE_TOOLS_ID}/async_poll/{job_id}?ending_update_only=true"

    done = False
    while not done:
        poll_response = requests.get(poll_url, headers=config.RELEVANCE_HEADERS).json()
        if poll_response['type'] == "complete" or poll_response['type'] == 'failed':
            done = True
            break
        time.sleep(3)

    # print(poll_response)
    
    return