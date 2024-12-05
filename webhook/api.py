import asyncio
import time
from fastapi import Request, Query, Response, APIRouter
from fastapi.responses import JSONResponse

from constants import MYTOKEN
from services.diffrentiate import diffrentiate_user_input
from services.messages import process_msg
from services.reminder import notifcation
from utils.fetch import send_message

route = APIRouter()

# Webhook verification
@route.get("/webhook")
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
@route.post("/webhook")
async def handle_webhook(request: Request):
    body_param = await request.json()
    print(f"Body Param | {body_param}")

    sender, msg, intent = process_msg(body_param)
    print("---"*10)
    response = diffrentiate_user_input(msg, sender, intent)
    send_message(sender.get("wa_id"), response)

def convert_time(timestamp):
    from datetime import datetime
    dt_object = datetime.fromtimestamp(int(timestamp))
    readable_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
    return str(readable_time)