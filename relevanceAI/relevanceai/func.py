import pdfkit
import markdown2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def markdown_to_pdf(markdown_content, output_pdf, wkhtmltopdf_path=None):
    # Convert markdown to HTML, ensuring it's UTF-8 encoded
    html_content = markdown2.markdown(markdown_content, extras=["tables"])

    # Make sure to specify the wkhtmltopdf path, if needed
    if wkhtmltopdf_path:
        config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_path)
        pdfkit.from_string(html_content, output_pdf, configuration=config, options={'encoding': 'UTF-8'})
    else:
        pdfkit.from_string(html_content, output_pdf, options={'encoding': 'UTF-8'})
        
def send_email_with_attachment(smtp_server, port, sender_email, sender_password, recipient_email, cc_emails, subject, body, attachment_path):
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['CC'] = ', '.join(cc_emails)  # Add CC recipients
    msg['Subject'] = subject

    # Attach the body text
    msg.attach(MIMEText(body, 'plain'))

    # Open the file to be sent as attachment
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