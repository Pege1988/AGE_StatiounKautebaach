import requests
from bs4 import BeautifulSoup
import csv
import sqlite3


# Fetch AGE data

def fetch_data(element, url):
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
def get_length(path):
    with open(path) as csvfile:
        reader = csv.reader(csvfile)
        reader_list = list(reader)
        return len(reader_list)

# Add data to CSV
def add_data_csv(path, time, value, datum_zait):
    fieldnames = ['ID', 'Time', 'Value', 'Datum an Auerzait']
    next_id = get_length(path)
    with open(path, "a", newline='') as csvfile: # "a" = append data
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({
            "ID": next_id,
            "Time": time,
            "Value": value,
            "Datum an Auerzait": datum_zait,
            })

# Add data to SQL
def add_data_sql(path, time, value, datum_zait):
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    cur.execute('INSERT INTO age (Time, Value, Datum_Auerzäit) VALUES (?, ?, ?)', (time, value, datum_zait))
    conn.commit()