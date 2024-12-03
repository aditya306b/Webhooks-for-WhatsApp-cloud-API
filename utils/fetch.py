import requests

from constants import TOKEN, URL,PHONE_ID

def fetch_data(url):
    try:
        res = requests.get(url, headers={"Authorization": f"Bearer {TOKEN}"})
        if res.status_code == 200:
            return res
        else:
            raise Exception(f"Error: {res.status_code}")
    except Exception as e:
        print(e)
        raise Exception("Error in fetching data")


def send_message(recipient: str, msg_body: str):
    try:
        url = f"{URL}/{PHONE_ID}/messages"
        headers = {"Content-Type": "application/json"}
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient,
            "text": {"body": f"{msg_body[:4095]}"}
        }
        res = requests.post(url, headers=headers, json=payload, params={"access_token": TOKEN})
        print(res.json())
        if res.json().get("error"):
            raise Exception("Error in sending message")
    except Exception as e:
        print(e)
        raise Exception("Error in sending message")