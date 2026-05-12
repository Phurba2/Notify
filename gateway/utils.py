import os, smtplib, requests
from email.message import EmailMessage

def send_real_email(recipient_email, message_body):
    try:
        msg = EmailMessage()
        msg.set_content(message_body)
        msg['Subject'] = "Django System Notification"
        msg['From'] = os.getenv("EMAIL_ADDRESS")
        msg['To'] = recipient_email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(os.getenv("EMAIL_ADDRESS"), os.getenv("EMAIL_PASSWORD"))
            smtp.send_message(msg)
        return True
    except:
        return False