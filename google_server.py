import json
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from constants import OWN_URL
from google_auth_oauthlib.flow import InstalledAppFlow

# Define the scopes and redirect URI
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

route = APIRouter()

# Route to start OAuth and get the authorization URL
@route.get("/start")
def start_oauth():
    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES, redirect_uri=OWN_URL)
    
    auth_url, _ = flow.authorization_url(prompt='consent')
    
    return JSONResponse(content={"auth_url": auth_url})


@route.get("/")
async def callback(code: str):
    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES, redirect_uri=OWN_URL)
    
    # Exchange the authorization code for credentials
    flow.fetch_token(authorization_response=f'{OWN_URL}/callback?code={code}')
    
    creds = flow.credentials
    
    with open('token.json', 'w') as token_file:
        token_file.write(creds.to_json())
    
    return {"access_token": creds.token, "refresh_token": creds.refresh_token, "expires_in": creds.expiry.isoformat()}
