import smtplib
from email.mime.text import MIMEText


def send_mail(email, subject, message):
    port = 2525
    smtp_server = 'smtp.mailtrap.io'
    login = '70ae89b6747f01'
    password = '38aeeb21ae2003'
    message = f"<h3>New Contact Submission</h3><ul><li>Email: {email}</li><li>Subject: {subject}</li><li>Message: {message}</li></ul>"

    sender_email = email
    receiver_email = 'email2@example.com'
    msg = MIMEText(message, 'html')
    msg['Subject'] = 'New Contact Approach You!'
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # Send email
    with smtplib.SMTP(smtp_server, port) as server:
        server.login(login, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
