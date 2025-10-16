import csv
import os

FLIGHTS_FILE = os.path.join('data', 'flights.csv')

def list_flights():
    flights = []
    with open(FLIGHTS_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            flights.append(row)
    return flights

def book_flight(flight_number):
    flights = list_flights()
    updated = []
    booked = False
    for flight in flights:
        if flight['FlightNumber'] == flight_number and int(flight['SeatsAvailable']) > 0:
            flight['SeatsAvailable'] = str(int(flight['SeatsAvailable']) - 1)
            booked = True
        updated.append(flight)
    if booked:
        with open(FLIGHTS_FILE, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=flights[0].keys())
            writer.writeheader()
            writer.writerows(updated)
    return booked
