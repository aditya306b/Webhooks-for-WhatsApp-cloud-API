import base64
from email.mime.text import MIMEText
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_server import start_oauth

# Assume you already have the access token

credentials = Credentials.from_authorized_user_file("token.json")

def create_email(to, subject, message_text):
    message = MIMEText(message_text)
    message['To'] = to
    message['Subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}

def send_mail(to, subject, body):
    try:
        service = build('gmail', 'v1', credentials=credentials)
        service.users().messages().send(userId='me', body=create_email(to, subject, body)).execute()
        return "Mail sent successfully"

    except Exception as e:
        if "The credentials do not contain" in str(e):
            res = start_oauth().body.decode()
            return json.loads(res).get("auth_url")
        else:
            print(f"Error sending mail: {e}")
            return "Error sending in mail contact Papa Pathak!"