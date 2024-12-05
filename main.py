from fastapi import FastAPI
from webhook.api import route as webhook_route
from google_server import route as mail_route

app = FastAPI()

app.include_router(webhook_route)
app.include_router(mail_route)

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
