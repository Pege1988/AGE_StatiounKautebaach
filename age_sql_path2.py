# Version 2.0.0

import requests
from bs4 import BeautifulSoup
import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import datetime
import sqlite3
import os

#==============================================================
#   PARAMETERS
#==============================================================

# Test parameter (if test local, else synology)
test = False

# Reference values for triggering alarms
ref_route = 120 # Reference for water levels under bridge
ref_pannels = 180 # Reference for installing flood pannels
ref_flooding = 220 # Reference when house starts flooding

# URL for weather station 14 @Kautenbach
url = 'https://www.inondations.lu/basins/sauer?station=14&show-details'

# Messages
Warnung = "Warnung: De Waasserpegel KB klëmmt!"
Entwarnung = "Entwarnung: De Waasserpegel KB fällt!"
Panneau = "Opgepasst: Panneau'en asetzen"
Iwwerschwemmung = "Iwwerschwemmunsgefoor"

# Filepaths
if test == True:
    folder_path = r"C:\Users\neo_1\Dropbox\Projects\Programing\AGE Statioun Kautebaach"
else:
    folder_path = "/volume1/homes/Pege_admin/Python_scripts"
    script_path = "/volume1/python_scripts/AGE_StatiounKautebaach"

csv_file = "age_wtht_ml.csv"
sql_file = "pege_db.sqlite"
conf_file = "confidential.txt"

csv_path = os.path.join(folder_path, csv_file)
sql_path = os.path.join(folder_path, sql_file)
conf_path = os.path.join(script_path, conf_file)

#==============================================================
#   FUNCTIONS
#==============================================================

# Fetch AGE data
def fetch_age_data(element):
    age_r = requests.get(url)
    age_soup = BeautifulSoup(age_r.text, 'html.parser')
    # Fetch data element
    data = age_soup.find_all('td', {'class': 'info-table-value compact'})[element].text
    data = data.replace('\n','').replace(' ','').replace('\r','') # To get rid of all the space and new rows 
    if element > 2:
        data = data.replace('cm','') 
        data = int(data)
    return(data)

# Get number of obs in CSV
def get_length():
    with open(csv_path) as csvfile:
        reader = csv.reader(csvfile)
        reader_list = list(reader)
        return len(reader_list)

# Add data to CSV
def add_data_csv():
    fieldnames = ['ID', 'Time', 'Value', 'Datum an Auerzait']
    next_id = get_length()
    with open(csv_path, "a", newline='') as csvfile: # "a" = append data
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({
            "ID": next_id,
            "Time": time_now,
            "Value": value_now,
            "Datum an Auerzait": datum_zait,
            })

# Add data to SQL
def add_data_sql():
    conn = sqlite3.connect(sql_path)
    cur = conn.cursor()
    cur.execute('INSERT INTO age (Time, Value, Datum_Auerzäit) VALUES (?, ?, ?)', (time_now, value_now, datum_zait))
    conn.commit()

# Send Mail
def send_mail(subject, recipient):
    host = "smtp-mail.outlook.com"
    port = 587
    password = confidential[1]
    sender = confidential[0]
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
                            <p>De Waasserpegel steet op """ + str(value_now) +""" cm.</p>
                            <p>Source: <a href="https://www.inondations.lu/basins/sauer?station=14&show-details">AGE - Waasserpegel Kautebaach</a></p>
                        </div>
                    </body>
                </html>"""
    part = MIMEText(message, "html")
    # Attach parts into message container.
    the_msg.attach(part)
    email_conn.sendmail(sender, recipient, the_msg.as_string())
    email_conn.quit()

# Send Alarm
def send_alarm():  
    if value_now >= ref_route and value_past < ref_route:
        if test == True:
            send_mail(Warnung, PJ)
        else:
            send_mail(Warnung, Tessy)
            send_mail(Warnung, PJ)
            send_mail(Warnung, Yves)
    elif value_now <= ref_route and value_past > ref_route:
        if test == True:
            send_mail(Entwarnung, PJ)
        else:
            send_mail(Entwarnung, PJ)
            send_mail(Entwarnung, Yves)
    if value_now >= ref_pannels and value_past < ref_pannels:
        if test == True:
            send_mail(Panneau, PJ)
        else:
            send_mail(Panneau, PJ)
    if value_now >= ref_flooding and value_past < ref_flooding:
        if test == True:
            send_mail(Iwwerschwemmung, PJ)
        else:
            send_mail(Iwwerschwemmung, PJ)

#==============================================================
#   SCRIPT
#==============================================================

# Get data from confidential file
confidential = []
with open(conf_path) as f:
    for line in f:
        confidential.append(line.replace("\n",""))

# Recipients
PJ = confidential[2]
Tessy = confidential[3]
Yves = confidential[4]

# Current and past time
time_now = fetch_age_data(1)
time_past = fetch_age_data(2)

# Current and past values
if test == True: 
    value_now = ref_route
    value_past = ref_route+1
else:
    value_now = fetch_age_data(3)
    value_past = fetch_age_data(4)

# To add date and time when data was retrieved
datum_zait = datetime.datetime.now() 

add_data_csv()
add_data_sql()
send_alarm()