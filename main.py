from fastapi import FastAPI, Request, Query, Response
import requests
from fastapi.responses import JSONResponse
import httpx
import os

app = FastAPI()

# Load environment variables
TOKEN = os.getenv("TOKEN")
MYTOKEN = os.getenv("MYTOKEN")

# Webhook verification
@app.get("/webhook")
async def verify_webhook(
    hub_mode: str = Query(None, alias="hub.mode"),
    hub_challenge: str = Query(None, alias="hub.challenge"),
    hub_verify_token: str = Query(None, alias="hub.verify_token")
):
    if hub_mode and hub_verify_token:
        if hub_mode == "subscribe" and hub_verify_token == MYTOKEN:
            print("Webhook verified")
            return Response(content=hub_challenge, status_code=200)
        else:
            return JSONResponse(status_code=403)

# Webhook handler
@app.post("/webhook")
async def handle_webhook(request: Request):
    body_param = await request.json()
    print(body_param)

    if body_param.get("object"):
        entry = body_param.get("entry", [{}])[0]
        changes = entry.get("changes", [{}])[0]
        value = changes.get("value", {})
        messages = value.get("messages", [{}])[0]

        if messages:
            phone_no_id = value.get("metadata", {}).get("phone_number_id")
            from_number = messages.get("from")
            msg_body = messages.get("text", {}).get("body")

            print(f"Phone number ID: {phone_no_id}")
            print(f"From: {from_number}")
            print(f"Message body: {msg_body}")

            if msg_body == "OTP":
                await send_message_with_template(phone_no_id, from_number, TOKEN)
            else:
                await send_message(phone_no_id, from_number, msg_body, TOKEN, body_param)

            return Response(status_code=200)

    return Response(status_code=404)

async def send_message_with_template(phone_no_id: str, recipient: str, token: str):
    url = f"https://graph.facebook.com/v13.0/{phone_no_id}/messages"
    headers = {"Content-Type": "application/json"}
    payload = {
        "messaging_product": "whatsapp",
        "to": recipient,
        "type": "template",
        "template": {
            "name": "otp",
            "language": {"code": "en"},
            "components": [
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": "123564"}
                    ]
                },
                {
                    "type": "button",
                    "sub_type": "url",
                    "index": 0,
                    "parameters": [
                        {"type": "text", "text": "123564"}
                    ]
                }
            ]
        }
    }
    async with httpx.AsyncClient() as client:
        await client.post(url, headers=headers, json=payload, params={"access_token": token})

async def send_message(phone_no_id: str, recipient: str, msg_body: str, token: str, body_param: dict):
    try:
        url = f"https://graph.facebook.com/v13.0/{phone_no_id}/messages"
        headers = {"Content-Type": "application/json"}
        payload = {
            "messaging_product": "whatsapp",
            "to": recipient,
            "text": {"body": f"Hi.. I'm Aditya, your message is : {msg_body}"}
        }
        res = requests.post(url, headers=headers, json=payload, params={"access_token": token})
        print(res.json())
        if res.json().get("error"):
            entry = body_param.get("entry", [{}])[0]
            changes = entry.get("changes", [{}])[0]
            value = changes.get("value", {})
            messages = value.get("messages", [{}])[0]
            number = messages.get("from")
            msg = messages.get("text", {}).get("body")
            name = body_param["entry"][0]["changes"][0]["value"]["contacts"][0]["profile"]["name"]

            owner = dict(payload)
            owner["to"] = "918103245232"
            owner["text"]["body"] = f"*ALERT!* \nWe recieved a message from unknown source\n*Identity* : {name} <{number}>\n*Message* : {msg}\n*Timestamp* : {convert_time(messages.get('timestamp'))}"
            requests.post(url, headers=headers, json=owner, params={"access_token": token})

    except Exception as e:
        print(e)

def convert_time(timestamp):
    from datetime import datetime
    dt_object = datetime.fromtimestamp(int(timestamp))
    readable_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
    return str(readable_time)

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
