# Version 3.1.0
import datetime
import age
import mail
from configparser import ConfigParser

#==============================================================
#   PARAMETERS
#==============================================================

config = ConfigParser()
config.read('config.ini')

# Test parameter (if test local, else synology)
test = True

# Reference values for triggering alarms
ref_route = int(config['station']['ref_route'])
ref_pannels = int(config['station']['ref_pannels'])
ref_flooding = int(config['station']['ref_flooding'])

# URL for weather station 14 @Kautenbach
url = config['station']['url']

Warnung = config['messages']['warnung']
Entwarnung = config['messages']['entwarnung']
Panneau = config['messages']['panneau']
Iwwerschwemmung = config['messages']['iwwerschwemmung']

csv_path = config['filepaths']['csv_path']
sql_path = config['filepaths']['sql_path']

# Recipients
user_1 = config['users']['user_1']
user_2 = config['users']['user_2']
user_3 = config['users']['user_3']

# Current and past time
time_now = age.fetch_data(2, url)
time_past = age.fetch_data(1, url)

# Current and past values

value_now = age.fetch_data(4, url)
value_past = age.fetch_data(3, url)

if test == True: 
    mail.send(Warnung, user_1, config['sender']['pw'], config['sender']['mail'], value_now)

# To add date and time when data was retrieved
datum_zait = datetime.datetime.now() 

age.add_data_csv(csv_path, time_now, value_now, datum_zait)
age.add_data_sql(sql_path, time_now, value_now, datum_zait)

if value_now >= ref_route and value_past < ref_route:
    mail.send(Warnung, user_1, config['sender']['pw'], config['sender']['mail'], value_now)
    mail.send(Warnung, user_2, config['sender']['pw'], config['sender']['mail'], value_now)
    mail.send(Warnung, user_3, config['sender']['pw'], config['sender']['mail'], value_now)
elif value_now <= ref_route and value_past > ref_route:
    mail.send(Entwarnung, user_1, config['sender']['pw'], config['sender']['mail'], value_now)
    mail.send(Warnung, user_2, config['sender']['pw'], config['sender']['mail'], value_now)
    mail.send(Entwarnung, user_3, config['sender']['pw'], config['sender']['mail'], value_now)
if value_now >= ref_pannels and value_past < ref_pannels:
    mail.send(Panneau, user_1, config['sender']['pw'], config['sender']['mail'], value_now)
if value_now >= ref_flooding and value_past < ref_flooding:
    mail.send(Iwwerschwemmung, user_1, config['sender']['pw'], config['sender']['mail'], value_now)