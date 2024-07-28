from twilio.rest import Client
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv()
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TTWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.environ[TWILIO_ACCOUNT_SID]
auth_token = os.environ[TWILIO_AUTH_TOKEN]
client = Client(account_sid, auth_token)

def tw_send_msg():
    message = client.messages.create(
    from_='whatsapp:+14155238886',
    body='123',
    to='whatsapp:+77086415391'
    )

    print(message.sid)

def main():
    tw_send_msg()

if __name__ == "__main__":
    main()