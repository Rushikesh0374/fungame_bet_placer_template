import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(body_text):
    # 🔐 Replace these with your actual credentials and info
    sender_email = "yogeshwaripolytechnic@gmail.com"
    receiver_email = "11r2r3r@gmail.com"
    app_password = "eopt ksav rthf jflh"  # App Password from Gmail

    subject = "Hello from Fungame EC2"
    body = f"Error in GK00230743: {body_text}"

    try:
        # Create email message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Connect to SMTP server and send email
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, app_password)
            server.send_message(msg)

        print("✅ Email sent successfully!")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

