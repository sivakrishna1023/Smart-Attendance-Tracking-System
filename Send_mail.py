# import smtplib
# from email.message import EmailMessage

# SENDER_EMAIL = "moruganti.phd2019.ece@nitrr.ac.in"
# APP_PASSWORD = "Madhu140886!"

# def send_mail_with_excel(recipient_email, subject, content, excel_file):
#     msg = EmailMessage()
#     msg['Subject'] = subject
#     msg['From'] = SENDER_EMAIL
#     msg['To'] = recipient_email
#     msg.set_content(content)

#     with open(excel_file, 'rb') as f:
#         file_data = f.read()
#     msg.add_attachment(file_data, maintype="application", subtype="csv", filename=excel_file)

#     with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
#         smtp.login(SENDER_EMAIL, APP_PASSWORD)
#         smtp.send_message(msg)
     

		
# recipient_email='aashujaiswal132@gmail.com'
# Date_='19012024'
# Professor_name_='TMEENPAL'
# content='Hi, PFA'

# excel_file='attendance_file.csv'


# subject=Date_+Professor_name_+'Attendance'	
# send_mail_with_excel(recipient_email, subject, content, excel_file)		


import smtplib
from email.message import EmailMessage
import os
import argparse

class EmailSender:
    def __init__(self, sender_email, app_password, recipient_email, subject, content, excel_file):
        """
        Initialize the parameters for sending an email.

        :param sender_email: Sender's email address.
        :param app_password: Application-specific password for authentication.
        :param recipient_email: Recipient's email address.
        :param subject: Subject of the email.
        :param content: Body content of the email.
        :param excel_file: Path to the Excel file to attach.
        """
        self.sender_email = sender_email
        self.app_password = app_password
        self.recipient_email = recipient_email
        self.subject = subject
        self.content = content
        self.excel_file = excel_file
    
    def send_mail(self):
        """
        Send an email with the specified Excel attachment.
        """
        msg = EmailMessage()
        msg['Subject'] = self.subject
        msg['From'] = self.sender_email
        msg['To'] = self.recipient_email
        msg.set_content(self.content)

        if os.path.exists(self.excel_file):
            with open(self.excel_file, 'rb') as f:
                file_data = f.read()
            msg.add_attachment(file_data, maintype="application", subtype="csv", filename=os.path.basename(self.excel_file))
            print(f"Attached file: {self.excel_file}")
        else:
            print(f"File not found: {self.excel_file}")
            return

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(self.sender_email, self.app_password)
            smtp.send_message(msg)
            print(f"Email sent to {self.recipient_email}.")

# Main function to parse arguments and run the email sender
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Send an email with an Excel attachment.')
    parser.add_argument('recipient_email', type=str, help='Recipient email address')
    parser.add_argument('subject', type=str, help='Email subject')
    parser.add_argument('content', type=str, help='Email body content')
    parser.add_argument('excel_file', type=str, help='Path to the Excel file to attach')
    
    args = parser.parse_args()

    # Initialize the EmailSender class with the provided arguments
    sender_email = "moruganti.phd2019.ece@nitrr.ac.in"
    app_password = "Madhu140886!"  # Replace this with a secure way of handling passwords

    email_sender = EmailSender(sender_email=sender_email, 
                               app_password=app_password, 
                               recipient_email=args.recipient_email, 
                               subject=args.subject, 
                               content=args.content, 
                               excel_file=args.excel_file)
    
    # Send the email
    email_sender.send_mail()

