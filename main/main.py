# Version 3.1.3
from configparser import ConfigParser
import age
import datetime
import mail

config = ConfigParser()
config.read('config.ini')

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

time_past = age.fetch_data(1, url)
time_now = age.fetch_data(2, url)
value_past = age.fetch_data(3, url)
value_now = age.fetch_data(4, url)
datum_zait = datetime.datetime.now() 

if config['local']['local'] == 'true': 
    mail.send("Wasserpegel Kautebaach Test", user_1, value_now)

age.add_data_csv(csv_path, time_now, value_now, datum_zait)
age.add_data_sql(sql_path, time_now, value_now, datum_zait)

if value_now >= ref_route and value_past < ref_route:
    mail.send(Warnung, user_1, value_now)
    mail.send(Warnung, user_2, value_now)
    mail.send(Warnung, user_3, value_now)
elif value_now <= ref_route and value_past > ref_route:
    mail.send(Entwarnung, user_1, value_now)
    mail.send(Entwarnung, user_2, value_now)
    mail.send(Entwarnung, user_3, value_now)
if value_now >= ref_pannels and value_past < ref_pannels:
    mail.send(Panneau, user_1, value_now)
if value_now >= ref_flooding and value_past < ref_flooding:
    mail.send(Iwwerschwemmung, user_1, value_now)