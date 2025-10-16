import csv
import os

USERS_FILE = os.path.join('data', 'users.csv')

def register(username, password):
    with open(USERS_FILE, 'a', newline='') as file:
        file.write(f"{username},{password}\n")
    return True

def login(username, password):
    with open(USERS_FILE, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['Username'] == username and row['Password'] == password:
                return True
    return False
