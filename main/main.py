# Version 2.1.0


import datetime
import os
import age
import mail

#==============================================================
#   PARAMETERS
#==============================================================

# Test parameter (if test local, else synology)
test = True

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
    folder_path = r"C:\Users\neo_1\Dropbox\Projects\Programing\AGE_StatiounKautebaach"
    script_path = r"C:\Users\neo_1\Dropbox\Projects\Programing\AGE_StatiounKautebaach"
else:
    folder_path = "/volume1/homes/Pege_admin/Python_scripts"
    script_path = "/volume1/python_scripts/AGE_StatiounKautebaach"

csv_file = "age_wtht_ml.csv"
sql_file = "pege_db.sqlite"
conf_file = "confidential.txt"

csv_path = os.path.join(folder_path, csv_file)
sql_path = os.path.join(folder_path, sql_file)
conf_path = os.path.join(script_path, conf_file)

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
time_now = age.fetch_data(2, url)
time_past = age.fetch_data(1, url)

# Current and past values
if test == True: 
    value_now = ref_route
    value_past = ref_route+1
else:
    value_now = age.fetch_data(4, url)
    value_past = age.fetch_data(3, url)

# To add date and time when data was retrieved
datum_zait = datetime.datetime.now() 

age.add_data_csv(csv_path, time_now, value_now, datum_zait)
age.add_data_sql(sql_path, time_now, value_now, datum_zait)

if value_now >= ref_route and value_past < ref_route:
    if test == True:
        mail.send(Warnung, PJ, confidential[1], confidential[0], value_now)
    else:
        mail.send(Warnung, Tessy, confidential[1], confidential[0], value_now)
        mail.send(Warnung, PJ, confidential[1], confidential[0], value_now)
        mail.send(Warnung, Yves, confidential[1], confidential[0], value_now)
elif value_now <= ref_route and value_past > ref_route:
    if test == True:
        mail.send(Entwarnung, PJ, confidential[1], confidential[0], value_now)
    else:
        mail.send(Entwarnung, PJ, confidential[1], confidential[0], value_now)
        mail.send(Entwarnung, Yves, confidential[1], confidential[0], value_now)
if value_now >= ref_pannels and value_past < ref_pannels:
    mail.send(Panneau, PJ, confidential[1], confidential[0], value_now)
if value_now >= ref_flooding and value_past < ref_flooding:
    mail.send(Iwwerschwemmung, PJ, confidential[1], confidential[0], value_now)