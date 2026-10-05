from fastapi import FastAPI
from src.api.schemas import NetworkEvent

app  = FastAPI()

@app.get("/")
def root():
    return {"message": "CyberShield-Auto API is running"}

@app.post("/events")
def create_event(event: NetworkEvent):
    return event



