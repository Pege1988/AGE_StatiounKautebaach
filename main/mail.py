from configparser import ConfigParser
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import jinja2
import smtplib 

config = ConfigParser()
config.read('config.ini')

def send(subject, recipient, value):
    host = config['sender']['host']
    port = int(config['sender']['port'])
    email_conn = smtplib.SMTP(host,port)
    email_conn.ehlo()
    email_conn.starttls()
    email_conn.login(config['sender']['mail'], config['sender']['pw'])
    the_msg = MIMEMultipart("alternative")
    the_msg['Subject'] = subject 
    the_msg["From"] = config['sender']['mail']
    the_msg["To"] = recipient
    # Create the body of the message
    css_file = open('templates/css.txt', 'r')
    css = css_file.read()
    template_loader = jinja2.FileSystemLoader(searchpath='templates')
    template_env = jinja2.Environment(loader=template_loader)
    main_template = template_env.get_template('html_message.html')
    main_html_var = {
        'css': css,
        'waterlevel': value
    }

    html = main_template.render(**main_html_var)
    part = MIMEText(html, "html")
    # Attach parts into message container.
    the_msg.attach(part)
    email_conn.sendmail(config['sender']['mail'], recipient, the_msg.as_string())
    email_conn.quit()


