from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# MySQL Connection
db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Mihir2701",
  database="transport"
)

# Create a cursor object to execute queries
cursor = db.cursor()

# Route to serve the HTML form
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle form submission
@app.route('/booking_confirm', methods=['POST'])
def booking_confirm():
    # Fetch form data
    booking_user = request.form['booking_user']
    sender_name = request.form['sender_name']
    pickup_address = request.form['pickup_address']
    receiver_name = request.form['receiver_name']
    delivery_address = request.form['delivery_address']
    package_description = request.form['package_description']

    # Insert data into MySQL
    sql = "INSERT INTO bookings (booking_user, sender_name, pickup_address, receiver_name, delivery_address, package_description) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (booking_user, sender_name, pickup_address, receiver_name, delivery_address, package_description)
    cursor.execute(sql, values)

    # Commit the transaction
    db.commit()

    return 'Booking confirmed successfully!'

if __name__ == '__main__':
    app.run(debug=True)
