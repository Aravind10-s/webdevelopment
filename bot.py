import smtplib
import schedule
import time
import requests

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Sender details
sender_email = "aravind123uu@gmail.com"
password = "modw hmdk xcqk udga"


# Receiver email
receivers = [
    "deepak.cherthala45@gmail.com"
]


def get_quote():

    try:
        response = requests.get(
            "https://zenquotes.io/api/random",
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        quote = data[0]["q"]
        author = data[0]["a"]

        return f"""
Today's Quote:

"{quote}"

- {author}
"""

    except Exception as e:
        return "Could not fetch quote: " + str(e)



def send_email():

    print("Sending email...")

    quote_message = get_quote()

    print("Quote fetched")

    for receiver in receivers:

        email = MIMEMultipart()

        email["From"] = sender_email
        email["To"] = receiver
        email["Subject"] = "Daily Motivational Quote"

        email.attach(
            MIMEText(quote_message, "plain")
        )


        try:
            server = smtplib.SMTP(
                "smtp.gmail.com",
                587
            )

            server.starttls()

            server.login(
                sender_email,
                password
            )

            server.sendmail(
                sender_email,
                receiver,
                email.as_string()
            )

            server.quit()

            print(
                "Email sent successfully to:",
                receiver
            )

        except Exception as e:
            print(
                "Email error:",
                e
            )


print("Daily quote email scheduler started...")


# Test immediately
send_email()


# Daily automatic sending
schedule.every().day.at("11:56").do(send_email)


while True:

    schedule.run_pending()

    time.sleep(60)
