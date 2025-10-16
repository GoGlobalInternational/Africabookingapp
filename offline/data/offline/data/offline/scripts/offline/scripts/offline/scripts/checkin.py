from datetime import datetime, timedelta
import csv
import os

FLIGHTS_FILE = os.path.join('data', 'flights.csv')

def checkin_possible(flight_number):
    with open(FLIGHTS_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['FlightNumber'] == flight_number:
                flight_time = datetime.strptime(row['Date'] + " " + row['Time'], "%Y-%m-%d %H:%M")
                if datetime.now() >= flight_time - timedelta(hours=24):
                    return True
    return False
