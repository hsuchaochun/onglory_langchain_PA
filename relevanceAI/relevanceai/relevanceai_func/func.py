import os
import time
import pdfkit
import smtplib
import requests
import markdown2
from datetime import datetime
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from config import config

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
        
    return

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
        
    return

def generate_attachment_path(prefix):
    date_folder = datetime.now().strftime("%Y%m%d")
    os.makedirs(f'./daily_summary/{date_folder}', exist_ok=True)
    return f'./daily_summary/{date_folder}/Onglory_{date_folder}_{prefix}.pdf'

def execute_relevance_agent(relevance_base_url, relevance_headers, agent_id, content):
    body = {
        "message": {
            "role": "user",
            "content": content
        },
        "agent_id": agent_id
    }
    
    response = requests.post(
        relevance_base_url + f"/agents/trigger", 
        headers=relevance_headers, 
        json=body
    )
    
    job = response.json()
    studio_id = job["job_info"]["studio_id"]
    job_id = job["job_info"]["job_id"]
    
    done = False
    status = None
    while not done:
        response = requests.get(
            relevance_base_url + f"/studios/{studio_id}/async_poll/{job_id}", 
            headers=relevance_headers
        )
        
        status = response.json()
        
        for update in status['updates']:
            if update['type'] == "chain-success":
                done = True
                break
            
        time.sleep(3)
        
    message = status['updates'][0]['output']['output']['answer']
    
    return job, message

def execute_relevance_tools(relevance_base_url, relevance_headers, project_id, tool_id, params):
    body = {
        "params": params,
        "project": project_id
    }
    
    response = requests.post(
        relevance_base_url + f"/studios/{tool_id}/trigger_async", 
        headers=relevance_headers, 
        json=body
    )
    
    # print(f'Tool {tool_id} triggered.')
    # print(f'Job response: {response.json()}')
    
    job = response.json()
    job_id = job['job_id']
    
    poll_url = relevance_base_url + f"/studios/{tool_id}/async_poll/{job_id}?ending_update_only=true"
    
    done = False
    while not done:
        poll_response = requests.get(poll_url, headers=relevance_headers).json()
        if poll_response['type'] == "complete" or poll_response['type'] == 'failed':
            done = True
            break
        time.sleep(3)
    
    # print(f'Pool response: {poll_response}')
    
    if 'output' in poll_response['updates'][0]:
        if 'transformed' in poll_response['updates'][0]['output']:
            return job, poll_response['updates'][0]['output']['transformed']
        elif 'answer' in poll_response['updates'][0]['output']:
            return job, poll_response['updates'][0]['output']['answer']
        else:
            return job, poll_response['updates'][0]['output']
    else:
        return job, None

def create_investment_summary_pdf_by_agent(attachment_path):
    content = "Onglory投資彙整"
    job, message = execute_relevance_agent(config.RELEVANCE_BASE_URL, config.RELEVANCE_HEADERS, config.RELEVANCE_INVESTMENT_SUMMARY_AGENT_ID, content)
    markdown_to_pdf(message, attachment_path, orientation='landscape')
    return

def create_financial_advice_pdf_by_agent(attachment_path):
    content = "Daily market recommendations."
    job, message = execute_relevance_agent(config.RELEVANCE_BASE_URL, config.RELEVANCE_HEADERS, config.RELEVANCE_FINANCIAL_ADVISE_AGENT_ID, content)
    markdown_to_pdf(message, attachment_path, orientation='landscape')
    return

def create_investment_summary_pdf_by_tool(attachment_path):
    job, response = execute_relevance_tools(config.RELEVANCE_BASE_URL, config.RELEVANCE_HEADERS, config.RELEVANCE_PROJECT_ID, config.RELEVANCE_INVESTMENT_SUMMARY_TOOL_ID, {})
    # print(response)
    markdown_to_pdf(response, attachment_path, orientation='landscape')
    return

def create_financial_advice_pdf_by_tool(attachment_path):
    job, response = execute_relevance_tools(config.RELEVANCE_BASE_URL, config.RELEVANCE_HEADERS, config.RELEVANCE_PROJECT_ID, config.RELEVANCE_FINANCIAL_ADVISE_TOOL_ID, {})
    # print(response)
    markdown_to_pdf(response, attachment_path, orientation='portrait')
    return

def create_and_send_daily_summary():
    investment_summary_path = generate_attachment_path("investment_summary")
    financial_advice_path = generate_attachment_path("financial_advice")
    
    # create_investment_summary_pdf_by_agent(investment_summary_path)
    # create_financial_advice_pdf_by_agent(financial_advice_path)
    create_investment_summary_pdf_by_tool(investment_summary_path)
    create_financial_advice_pdf_by_tool(financial_advice_path)
    
    attachment_paths = [investment_summary_path, financial_advice_path]
    
    subject = "Onglory Crypto Daily Summary"
    body = "Please find the attached files."
    
    send_email_with_attachment(
        config.SMTP_SERVER, config.SSL_PORT, 
        config.SENDER_EMAIL, config.SENDER_EMAIL_PASSWORD, 
        config.RECIPIENT_EMAIL, config.CC_EMAILS, 
        subject, body, attachment_paths
    )
    
    return
    
def news_categorize(number=1, interval="HOUR"):
    job, poll_response = execute_relevance_tools(config.RELEVANCE_BASE_URL, config.RELEVANCE_HEADERS, config.RELEVANCE_PROJECT_ID, config.RELEVANCE_NEWS_CATEGORIZE_TOOL_ID, {
        "number": number, 
        "interval": interval
    })

    # print(poll_response)
    
    return