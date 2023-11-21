from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def send(subject, recipient, password, sender, value):
    host = "smtp-mail.outlook.com"
    port = 587
    email_conn = smtplib.SMTP(host,port)
    email_conn.ehlo()
    email_conn.starttls()
    email_conn.login(sender, password)
    the_msg = MIMEMultipart("alternative")
    the_msg['Subject'] = subject 
    the_msg["From"] = sender
    the_msg["To"] = recipient
    # Create the body of the message
    message = """<html>
                    <head>
                        <title>Waasserpegel Kautebaach</title>
                    </head>
                    <body>
                        <div>
                            <p>De Waasserpegel steet op """ + str(value) +""" cm.</p>
                            <p>Source: <a href="https://www.inondations.lu/basins/sauer?station=14&show-details">AGE - Waasserpegel Kautebaach</a></p>
                        </div>
                    </body>
                </html>"""
    part = MIMEText(message, "html")
    # Attach parts into message container.
    the_msg.attach(part)
    email_conn.sendmail(sender, recipient, the_msg.as_string())
    email_conn.quit()