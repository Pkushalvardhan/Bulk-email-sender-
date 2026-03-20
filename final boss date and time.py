import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import time

# Email credentials
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "nnm23vl040@nmamit.in"  # Replace with your email
SENDER_PASSWORD = "brxk wjju tjvu jfyq"  # Replace with your App Password

# Email content
subject = "Scheduled Email"
body = """\
Hi {name},

This is a test email sent using Python's smtplib, scheduled for a specific date and time.

Best regards,
Your Name
"""

# Input recipient email addresses
print("Enter recipient email addresses separated by commas:")
recipient_input = input("Recipients: ").strip()
recipients = [email.strip() for email in recipient_input.split(",") if "@" in email]

if not recipients:
    print("No valid email addresses provided.")
else:
    print(f"Recipients: {recipients}")

# Input scheduled time
print("Enter the scheduled time in the format YYYY-MM-DD HH:MM (e.g., 2024-11-25 15:33):")
try:
    scheduled_time_input = input("Scheduled Time: ").strip()
    scheduled_time = datetime.strptime(scheduled_time_input, "%Y-%m-%d %H:%M")
    print(f"Scheduled time is set to: {scheduled_time}")
except ValueError:
    print("Invalid date-time format. Please run the script again with the correct format.")
    scheduled_time = None  # Set to None for further graceful handling

# Function to wait until the scheduled time
def wait_until(target_time):
    """Pause the script until the target time is reached."""
    while datetime.now() < target_time:
        time.sleep(1)  # Check every second
    print("It's time to send the emails!")

# Main email sending logic
if scheduled_time:
    if datetime.now() > scheduled_time:
        # Notify that the time has been exceeded
        print("The scheduled time has already passed. Emails will not be sent.")
    else:
        try:
            # Wait until the scheduled time
            wait_until(scheduled_time)

            # Connect to the SMTP server
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.ehlo()  # Greet the server
            server.starttls()  # Upgrade to a secure connection
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            print("Logged in successfully.")

            # Send email to each recipient
            for recipient in recipients:
                personalized_body = body.format(name=recipient.split("@")[0])

                # Create the email
                msg = MIMEMultipart()
                msg["From"] = SENDER_EMAIL
                msg["To"] = recipient
                msg["Subject"] = subject
                msg.attach(MIMEText(personalized_body, "plain"))

                # Send email
                server.sendmail(SENDER_EMAIL, recipient, msg.as_string())
                print(f"Email successfully sent to {recipient}")

            print("All emails sent successfully.")

        except smtplib.SMTPAuthenticationError:
            print("Authentication error: Check your email and App Password settings.")
        except smtplib.SMTPRecipientsRefused as e:
            print(f"Recipient address refused: {e}")
        except smtplib.SMTPException as e:
            print(f"SMTP error occurred: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            # Ensure server connection is properly closed
            if 'server' in locals() and hasattr(server, 'quit'):
                try:
                    server.quit()
                    print("Server connection closed.")
                except Exception as e:
                    print(f"Failed to close the server connection: {e}")
else:
    print("Script exited due to invalid input.")
