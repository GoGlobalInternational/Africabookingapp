import tkinter as tk
from tkinter import messagebox, simpledialog
from scripts import auth, booking, checkin

def login_screen():
    username = simpledialog.askstring("Login", "Enter username:")
    password = simpledialog.askstring("Login", "Enter password:", show='*')
    if auth.login(username, password):
        messagebox.showinfo("Login", f"Welcome {username}!")
        main_menu()
    else:
        messagebox.showerror("Login", "Invalid credentials")

def register_screen():
    username = simpledialog.askstring("Register", "Choose username:")
    password = simpledialog.askstring("Register", "Choose password:", show='*')
    auth.register(username, password)
    messagebox.showinfo("Register", f"User {username} registered!")

def main_menu():
    menu = tk.Toplevel(root)
    menu.title("Africabookingapp Menu")
    
    tk.Button(menu, text="List Flights", command=list_flights_screen).pack(pady=5)
    tk.Button(menu, text="Book Flight", command=book_flight_screen).pack(pady=5)
    tk.Button(menu, text="Check-in", command=checkin_screen).pack(pady=5)
    tk.Button(menu, text="Logout", command=menu.destroy).pack(pady=5)

def list_flights_screen():
    flights = booking.list_flights()
    msg = "\n".join([f"{f['FlightNumber']}: {f['From']} -> {f['To']} | {f['Date']} {f['Time']} | Seats: {f['SeatsAvailable']} | Price: ${f['Price']}" for f in flights])
    messagebox.showinfo("Available Flights", msg)

def book_flight_screen():
    flight_number = simpledialog.askstring("Book Flight", "Enter flight number to book:")
    if booking.book_flight(flight_number):
        messagebox.showinfo("Booking", f"Flight {flight_number} booked successfully!")
    else:
        messagebox.showerror("Booking", "Booking failed. Flight full or not found.")

def checkin_screen():
    flight_number = simpledialog.askstring("Check-in", "Enter flight number to check-in:")
    if checkin.checkin_possible(flight_number):
        messagebox.showinfo("Check-in", f"Check-in successful for flight {flight_number}!")
    else:
        messagebox.showerror("Check-in", "Check-in not allowed yet.")

# Main Window
root = tk.Tk()
root.title("Africabookingapp")
root.geometry("400x200")

tk.Button(root, text="Login", command=login_screen).pack(pady=10)
tk.Button(root, text="Register", command=register_screen).pack(pady=10)

root.mainloop()
