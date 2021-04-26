import smtplib
import ssl
from constants import email_login, email_password
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(message):
    port = 587  # For starttls
    smtp_server = "smtp.gmail.com"
    sender_email = email_login
    receiver_email = email_login
    context = ssl.create_default_context()
    msg = MIMEMultipart()
    msg["Subject"] = Header("Семейная привлекательность - новый заказ")
    msg["From"] = Header(email_login)
    msg["To"] = Header(email_login)
    text = MIMEText(message, 'html')
    msg.attach(text)
    with smtplib.SMTP(smtp_server, port) as server:
        server.ehlo()  # Can be omitted
        server.starttls(context=context)
        server.ehlo()  # Can be omitted
        server.login(sender_email, email_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
    return True
