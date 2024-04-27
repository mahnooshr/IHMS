from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Connect to SQLite database
conn = sqlite3.connect('appointments.db', check_same_thread=False)
c = conn.cursor()

# Create appointments table if not exists
c.execute('''CREATE TABLE IF NOT EXISTS appointments
             (id INTEGER PRIMARY KEY, patient_name TEXT, doctor_name TEXT, appointment_date TEXT)''')
conn.commit()

@app.route('/book_appointment', methods=['POST'])
def book_appointment():
    data = request.json
    if data:
        patient_name = data.get('patient_name')
        doctor_name = data.get('doctor_name')
        appointment_date = data.get('appointment_date')

        # Check if appointment date is valid and available
        if is_valid_date(appointment_date) and is_available(appointment_date):
            # Book the appointment
            c.execute("INSERT INTO appointments (patient_name, doctor_name, appointment_date) VALUES (?, ?, ?)",
                      (patient_name, doctor_name, appointment_date))
            conn.commit()
            return jsonify({"message": "Appointment booked successfully."}), 200
        else:
            return jsonify({"error": "Invalid date or appointment not available."}), 400
    else:
        return jsonify({"error": "Invalid request data."}), 400

def is_valid_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def is_available(date_str):
    c.execute("SELECT * FROM appointments WHERE appointment_date=?", (date_str,))
    if c.fetchone():
        return False
    return True

if __name__ == '__main__':
    app.run(debug=True)
