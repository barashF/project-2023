from email.mime.multipart import MIMEMultipart

from email.mime.text import MIMEText

import smtplib

def sender_mail(to, sub, messaget):

    msg = MIMEMultipart()

    message = messaget

    password = "olsmxhuxxybhqekq"

    msg['From'] = "status.stack.market@gmail.com"

    msg['To'] = to

    msg['Subject'] = sub

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP('smtp.gmail.com: 587')

    server.starttls()

    server.login(msg['From'], password)

    server.sendmail(msg['From'], msg['To'], msg.as_string())

    server.quit()