
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# ---------------------------
# CONFIGURE YOUR GMAIL HERE
# ---------------------------
EMAIL_ADDRESS = "pischalifestyleacademy@gmail.com"
EMAIL_PASSWORD = "qohi kxyp tabp huea"    # Use the Gmail App Password

def send_email(name, email, phone):
    """Send form details to your Gmail inbox."""

    subject = "New Form Submission"
    body = f"""
A new user submitted the form:

Name: {name}
Email: {email}
Phone: {phone}
"""

    msg = MIMEMultipart()
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = EMAIL_ADDRESS
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        # Use SSL (more stable on Windows & Nigerian networks)
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)

        print("Email sent successfully!")

    except Exception as e:
        print("Error sending email:", e)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit_form():
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')

        print("--- NEW SIGNUP ---")
        print("Name:", name)
        print("Email:", email)
        print("Phone:", phone)

        # Send email
        send_email(name, email, phone)

        return redirect(url_for('thank_you'))

    return redirect(url_for('index'))


@app.route('/thank-you')
def thank_you():
    return render_template('thank-you.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
