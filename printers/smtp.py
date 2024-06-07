import copy
import csv
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_report(filename):
    subject = "xxx"
    sender_email = "xxx"
    smtp_server = "xxx"
    password = "xxx"
    body = """
        Hello,
        This is an automatically generated recently printed PDF report.
    """

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )

    message.attach(part)

    # Load CSV file and send emails
    context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, 587) as server:
        server.starttls(context=context)
        server.login(sender_email, password)

        with open('contacts_file.csv') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for name, email in reader:
                # Create a copy of the message for each recipient
                personalized_message = copy.deepcopy(message)
                personalized_message["To"] = email
                # Update the greeting with the recipient's name

                # Send the email
                server.sendmail(sender_email, email, personalized_message.as_string())


send_report('report.pdf')
