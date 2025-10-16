from flask import Flask, render_template, request, redirect, session, url_for, flash
import csv
import os
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "AfricabookingappSecret"

DATA_FOLDER = os.path.join(os.getcwd(), 'data')
USERS_FILE = os.path.join(DATA_FOLDER, 'users.csv')
FLIGHTS_FILE = os.path.join(DATA_FOLDER, 'flights.csv')

# -------------------
# Helper functions
# -------------------
def load_users():
    users = []
    with open(USERS_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            users.append(row)
    return users

def save_user(username, password):
    with open(USERS_FILE, 'a', newline='') as file:
        file.write(f"{username},{password}\n")

def load_flights():
    flights = []
    with open(FLIGHTS_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            flights.append(row)
    return flights

def save_flights(flights):
    with open(FLIGHTS_FILE, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=flights[0].keys())
        writer.writeheader()
        writer.writerows(flights)

def check_credentials(username, password):
    for user in load_users():
        if user['Username'] == username and user['Password'] == password:
            return True
    return False

def book_flight(flight_number):
    flights = load_flights()
    booked = False
    for flight in flights:
        if flight['FlightNumber'] == flight_number and int(flight['SeatsAvailable']) > 0:
            flight['SeatsAvailable'] = str(int(flight['SeatsAvailable']) - 1)
            booked = True
    if booked:
        save_flights(flights)
    return booked

def checkin_possible(flight_number):
    flights = load_flights()
    for flight in flights:
        if flight['FlightNumber'] == flight_number:
            flight_time = datetime.strptime(f"{flight['Date']} {flight['Time']}", "%Y-%m-%d %H:%M")
            if datetime.now() >= flight_time - timedelta(hours=24):
                return True
    return False

# -------------------
# Routes
# -------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        save_user(username, password)
        flash("Registration successful! Please login.")
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if check_credentials(username, password):
            session['username'] = username
            return redirect(url_for('flights'))
        else:
            flash("Invalid credentials")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/flights')
def flights():
    if 'username' not in session:
        return redirect(url_for('login'))
    flights = load_flights()
    return render_template('flights.html', flights=flights)

@app.route('/book/<flight_number>')
def book(flight_number):
    if 'username' not in session:
        return redirect(url_for('login'))
    if book_flight(flight_number):
        flash(f"Flight {flight_number} booked successfully!")
    else:
        flash(f"Booking failed for {flight_number}")
    return redirect(url_for('flights'))

@app.route('/checkin/<flight_number>')
def checkin(flight_number):
    if 'username' not in session:
        return redirect(url_for('login'))
    if checkin_possible(flight_number):
        flash(f"Check-in successful for flight {flight_number}")
    else:
        flash(f"Check-in not allowed yet for {flight_number}")
    return redirect(url_for('flights'))

if __name__ == '__main__':
    app.run(debug=True)
