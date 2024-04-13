from flask import Flask, request, jsonify,render_template,make_response
from sql_connection import get_sql_connection_cursor
from email.message import EmailMessage
import ssl
import smtplib
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from datetime import datetime


app = Flask(__name__)
app = Flask(__name__, static_url_path='/static')
email_sender="transportiocompany@gmail.com"
email_password="gjnm lpba lrhy nzvl"



# Establish database connection
connection = get_sql_connection_cursor()

@app.route('/checkAndSendEmail', methods=['POST'])
def sendemail():
    email_test = request.form.get('email')

    cursor = connection.cursor()

    # Check if email exists in road table
    query_road = "SELECT sender_name_road, receiver_name_road, delivery_add_road, desc_road FROM road WHERE email_road = %s"
    cursor.execute(query_road, (email_test,))
    road_orders = cursor.fetchall()

    # Check if email exists in ocean table
    query_ocean = "SELECT sender_name_ocean, receiver_name_ocean, delivery_add_ocean, desc_ocean FROM ocean WHERE email_ocean = %s"
    cursor.execute(query_ocean, (email_test,))
    ocean_orders = cursor.fetchall()

    # Check if email exists in air table
    query_air = "SELECT sender_name_air, receiver_name_air, delivery_add_air, desc_air FROM air WHERE email_air = %s"
    cursor.execute(query_air, (email_test,))
    air_orders = cursor.fetchall()

    # Construct email body
    body = ""

    for order in road_orders:
        body += "Road Freight Details:\n"
        for key, value in zip(['Sender Name', 'Receiver Name', 'Delivery Address', 'Cargo Description'], order):
            body += f"    {key}: {value}\n"
        body += "\n"

    for order in ocean_orders:
        body += "Ocean Freight Details:\n"
        for key, value in zip(['Sender Name', 'Receiver Name', 'Delivery Address', 'Cargo Description'], order):
            body += f"    {key}: {value}\n"
        body += "\n"

    for order in air_orders:
        body += "Air Freight Details:\n"
        for key, value in zip(['Sender Name', 'Receiver Name', 'Delivery Address', 'Cargo Description'], order):
            body += f"    {key}: {value}\n"
        body += "\n"


    # If email found in any table, send email
    if road_orders or ocean_orders or air_orders:
        em = EmailMessage()
        em['From'] = email_sender
        em['To'] = email_test
        em.set_content(body)

        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(email_sender, email_password)
            smtp.sendmail(email_sender, email_test, em.as_string())
            return render_template('email.html')
    else:
        return render_template('unsuccessfull.html')

@app.route('/generate_road_pdf', methods=['GET'])
def generate_road_pdf():
    # Fetch the latest row from the road table
    cursor = connection.cursor()
    query = "SELECT sender_name_road, receiver_name_road, delivery_add_road, desc_road FROM road ORDER BY id_road DESC LIMIT 1"
    cursor.execute(query)
    latest_road_order = cursor.fetchone()

    if latest_road_order:
        # Extract information from the latest row
        sender_name = latest_road_order[0]
        receiver_name = latest_road_order[1]
        delivery_address = latest_road_order[2]
        description = latest_road_order[3]
        freight_type = 'Road Freight'

        # Get current date and time
        current_datetime = datetime.now().strftime("%Y-%m-%d / %H:%M:%S")

        # Create PDF
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
        styles = getSampleStyleSheet()

        # Define custom styles
        title_style = styles["Title"]
        title_style.alignment = 1  # Center alignment
        title_style.fontSize = 18
        title_style.textColor = colors.black

        content_style = ParagraphStyle(
            "BodyText",
            parent=styles["Normal"],
            spaceAfter=12,
            fontSize=12,
        )

        subtitle_style = ParagraphStyle(
            "Subtitle",
            parent=styles["Normal"],
            fontSize=14,
            textColor=colors.black,
            alignment=1,
        )

        # Define content
        content = []
        content.append(Paragraph("Transportio", title_style))
        content.append(Spacer(1, 30))  # Add space below the title
        image_path = 'static/assets/images/feature-icon-1.png'  # Replace with the actual path to the image
        content.append(Image(image_path, width=120, height=120))
        content.append(Spacer(1, 25))  # Add space below the subtitle
        content.append(Paragraph("<b>Booking Receipt</b>", subtitle_style))
        content.append(Spacer(1, 25))  # Add space below the image
        content.append(Paragraph("<b>Sender Name:</b> {}".format(sender_name), content_style))
        content.append(Paragraph("<b>Receiver Name:</b> {}".format(receiver_name), content_style))
        content.append(Paragraph("<b>Delivery Address:</b> {}".format(delivery_address), content_style))
        content.append(Paragraph("<b>Package Description:</b> {}".format(description), content_style))
        content.append(Paragraph("<b>Type of Freight:</b> {}".format(freight_type), content_style))
        content.append(Paragraph("<b>Date and Time:</b> {}".format(current_datetime), content_style))

        # Add content to PDF
        doc.build(content)

        # Prepare response with PDF
        pdf_buffer.seek(0)
        response = make_response(pdf_buffer.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=receipt.pdf'
        return response
    else:
        return "No data found in the road table."
    
@app.route('/generate_ocean_pdf', methods=['GET'])
def generate_ocean_pdf():
    # Fetch the latest row from the ocean table
    cursor = connection.cursor()
    query = "SELECT sender_name_ocean, receiver_name_ocean, delivery_add_ocean, desc_ocean FROM ocean ORDER BY id_ocean DESC LIMIT 1"
    cursor.execute(query)
    latest_ocean_order = cursor.fetchone()

    if latest_ocean_order:
        # Extract information from the latest row
        sender_name = latest_ocean_order[0]
        receiver_name = latest_ocean_order[1]
        delivery_address = latest_ocean_order[2]
        description = latest_ocean_order[3]
        freight_type = 'Ocean Freight'

        # Get current date and time
        current_datetime = datetime.now().strftime("%Y-%m-%d / %H:%M:%S")

        # Create PDF
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
        styles = getSampleStyleSheet()

        # Define custom styles
        title_style = styles["Title"]
        title_style.alignment = 1  # Center alignment
        title_style.fontSize = 18
        title_style.textColor = colors.black

        content_style = ParagraphStyle(
            "BodyText",
            parent=styles["Normal"],
            spaceAfter=12,
            fontSize=12,
        )

        subtitle_style = ParagraphStyle(
            "Subtitle",
            parent=styles["Normal"],
            fontSize=14,
            textColor=colors.black,
            alignment=1,
        )

        # Define content
        content = []
        content.append(Paragraph("Transportio", title_style))
        content.append(Spacer(1, 30))  # Add space below the title
        image_path = 'static/assets/images/feature-icon-1.png'  # Replace with the actual path to the image
        content.append(Image(image_path, width=120, height=120))
        content.append(Spacer(1, 25))  # Add space below the subtitle
        content.append(Paragraph("<b>Booking Receipt</b>", subtitle_style))
        content.append(Spacer(1, 25))  # Add space below the image
        content.append(Paragraph("<b>Sender Name:</b> {}".format(sender_name), content_style))
        content.append(Paragraph("<b>Receiver Name:</b> {}".format(receiver_name), content_style))
        content.append(Paragraph("<b>Delivery Address:</b> {}".format(delivery_address), content_style))
        content.append(Paragraph("<b>Package Description:</b> {}".format(description), content_style))
        content.append(Paragraph("<b>Type of Freight:</b> {}".format(freight_type), content_style))
        content.append(Paragraph("<b>Date and Time:</b> {}".format(current_datetime), content_style))

        # Add content to PDF
        doc.build(content)

        # Prepare response with PDF
        pdf_buffer.seek(0)
        response = make_response(pdf_buffer.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=receipt.pdf'
        return response
    else:
        return "No data found in the ocean table."
    
@app.route('/generate_air_pdf', methods=['GET'])
def generate_air_pdf():
    # Fetch the latest row from the air table
    cursor = connection.cursor()
    query = "SELECT sender_name_air, receiver_name_air, delivery_add_air, desc_air FROM air ORDER BY id_air DESC LIMIT 1"
    cursor.execute(query)
    latest_air_order = cursor.fetchone()

    if latest_air_order:
        # Extract information from the latest row
        sender_name = latest_air_order[0]
        receiver_name = latest_air_order[1]
        delivery_address = latest_air_order[2]
        description = latest_air_order[3]
        freight_type = 'Air Freight'

        # Get current date and time
        current_datetime = datetime.now().strftime("%Y-%m-%d / %H:%M:%S")

        # Create PDF
        pdf_buffer = BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
        styles = getSampleStyleSheet()

        # Define custom styles
        title_style = styles["Title"]
        title_style.alignment = 1  # Center alignment
        title_style.fontSize = 18
        title_style.textColor = colors.black

        content_style = ParagraphStyle(
            "BodyText",
            parent=styles["Normal"],
            spaceAfter=12,
            fontSize=12,
        )

        subtitle_style = ParagraphStyle(
            "Subtitle",
            parent=styles["Normal"],
            fontSize=14,
            textColor=colors.black,
            alignment=1,
        )

        # Define content
        content = []
        content.append(Paragraph("Transportio", title_style))
        content.append(Spacer(1, 30))  # Add space below the title
        image_path = 'static/assets/images/feature-icon-1.png'  # Replace with the actual path to the image
        content.append(Image(image_path, width=120, height=120))
        content.append(Spacer(1, 25))  # Add space below the subtitle
        content.append(Paragraph("<b>Booking Receipt</b>", subtitle_style))
        content.append(Spacer(1, 25))  # Add space below the image
        content.append(Paragraph("<b>Sender Name:</b> {}".format(sender_name), content_style))
        content.append(Paragraph("<b>Receiver Name:</b> {}".format(receiver_name), content_style))
        content.append(Paragraph("<b>Delivery Address:</b> {}".format(delivery_address), content_style))
        content.append(Paragraph("<b>Package Description:</b> {}".format(description), content_style))
        content.append(Paragraph("<b>Type of Freight:</b> {}".format(freight_type), content_style))
        content.append(Paragraph("<b>Date and Time:</b> {}".format(current_datetime), content_style))

        # Add content to PDF
        doc.build(content)

        # Prepare response with PDF
        pdf_buffer.seek(0)
        response = make_response(pdf_buffer.getvalue())
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = 'attachment; filename=receipt.pdf'
        return response
    else:
        return "No data found in the air table."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/roadFreight', methods=['POST'])
def road_freight():
    try:
        # Extract form data
        email = request.form.get('email_road')
        # Extract other form fields similarly

        # Insert data into the database
        # Ensure that the keys in request.form match the column names in your database
        cursor = connection.cursor()
        query = ("INSERT INTO road "
                 "(email_road, sender_name_road, pickup_add_road, receiver_name_road, delivery_add_road, desc_road)"
                 "VALUES (%s, %s, %s, %s, %s, %s)")
        data = (email, request.form.get('sender_name_road'), request.form.get('pickup_add_road'), request.form.get('receiver_name_road'), request.form.get('delivery_add_road'), request.form.get('desc_road'))

        cursor.execute(query, data)
        connection.commit()

        # Optionally, return a response
        return render_template('success_road.html')

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/oceanFreight', methods=['POST'])
def ocean_freight():
    try:
        # Extract form data
        email = request.form.get('email_ocean')
        # Extract other form fields similarly

        # Insert data into the database
        # Ensure that the keys in request.form match the column names in your database
        cursor = connection.cursor()
        query = ("INSERT INTO ocean "
                 "(email_ocean, sender_name_ocean, pickup_add_ocean, receiver_name_ocean, delivery_add_ocean, desc_ocean)"
                 "VALUES (%s, %s, %s, %s, %s, %s)")
        data = (email, request.form.get('sender_name_ocean'), request.form.get('pickup_add_ocean'), request.form.get('receiver_name_ocean'), request.form.get('delivery_add_ocean'), request.form.get('desc_ocean'))

        cursor.execute(query, data)
        connection.commit()

        # Optionally, return a response
        return render_template('success_ocean.html')

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/airFreight', methods=['POST'])
def air_freight():
    try:
        # Extract form data
        email = request.form.get('email_air')
        # Extract other form fields similarly

        # Insert data into the database
        # Ensure that the keys in request.form match the column names in your database
        cursor = connection.cursor()
        query = ("INSERT INTO air "
                 "(email_air, sender_name_air, pickup_add_air, receiver_name_air, delivery_add_air, desc_air)"
                 "VALUES (%s, %s, %s, %s, %s, %s)")
        data = (email, request.form.get('sender_name_air'), request.form.get('pickup_add_air'), request.form.get('receiver_name_air'), request.form.get('delivery_add_air'), request.form.get('desc_air'))

        cursor.execute(query, data)
        connection.commit()

        # Optionally, return a response
        return render_template('success_air.html')

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/main', methods=['GET'])

def index():
    return render_template('index.html')

@app.route('/road', methods=['GET'])
def road():
    return render_template('road.html')

@app.route('/ocean', methods=['GET'])
def ocean():
    return render_template('ocean.html')

@app.route('/air', methods=['GET'])
def air():
    return render_template('air.html')

@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')

@app.route('/track', methods=['GET'])
def track():
    return render_template('tracking.html')
@app.route('/multiple', methods=['GET'])
def warehouse():
    return render_template('multiple.html')

if __name__ == "__main__":
    app.run(port=5000)

