############################# for testing email with gmail 

# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from email.mime.application import MIMEApplication

# def send_email_with_pdf(subject: str, recipient: str, html_content: str, pdf_bytes: bytes, pdf_filename: str):
# EMAIL = "ayush2211207@gmail.com"        # Replace with YOUR Gmail
# PASSWORD = "rdsi yozj tkbx okgj"              

#     msg = MIMEMultipart()
#     msg["From"] = sender
#     msg["To"] = recipient
#     msg["Subject"] = subject

#     # Attach HTML
#     msg.attach(MIMEText(html_content, "html"))

#     # Attach PDF
#     pdf_part = MIMEApplication(pdf_bytes, _subtype="pdf")
#     pdf_part.add_header("Content-Disposition", "attachment", filename=pdf_filename)
#     msg.attach(pdf_part)

#     with smtplib.SMTP("smtp.gmail.com", 587) as server:
#         server.starttls()
#         server.login(sender, password)
#         server.send_message(msg)




import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


def send_email_with_pdf(subject: str, recipient: str, html_content: str, pdf_bytes: bytes, pdf_filename: str):
    sender = "noreply@immiinfo.com"
    password = "ImmInfo@2025Secure"

    # Create the email
    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = recipient
    msg["Subject"] = subject

    msg.attach(MIMEText(html_content, "html"))

    # Attach PDF
    pdf_part = MIMEApplication(pdf_bytes, _subtype="pdf")
    pdf_part.add_header("Content-Disposition", "attachment", filename=pdf_filename)
    msg.attach(pdf_part)

    # Connect securely using STARTTLS (587)
    with smtplib.SMTP("smtpout.secureserver.net", 587, timeout=30) as server:
        server.ehlo()
        server.starttls(context=ssl.create_default_context())
        server.ehlo()
        server.login(sender, password)
        server.send_message(msg)
        print("✅ Email sent successfully via GoDaddy SMTP")


