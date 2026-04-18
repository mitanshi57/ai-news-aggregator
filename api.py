from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from sqlalchemy.exc import IntegrityError
from app.services.database import init_db, get_db
from app.models import Subscriber
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=FileResponse)
def home():
    return "static/index.html"
# Allow requests from any website (needed for the signup form)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# This runs when the server starts
@app.on_event("startup")
def startup():
    init_db()

# Define what a subscription request looks like
class SubscribeRequest(BaseModel):
    email: EmailStr


@app.post("/subscribe")
def subscribe(request: SubscribeRequest):
    db = next(get_db())
    try:
        subscriber = Subscriber(email=request.email)
        db.add(subscriber)
        db.commit()
        return {"message": f"Successfully subscribed {request.email}!"}
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="This email is already subscribed!")

@app.delete("/unsubscribe")
def unsubscribe(request: SubscribeRequest):
    db = next(get_db())
    subscriber = db.query(Subscriber).filter_by(email=request.email).first()
    if not subscriber:
        raise HTTPException(status_code=404, detail="Email not found!")
    subscriber.is_active = False
    db.commit()
    return {"message": f"Successfully unsubscribed {request.email}!"}

@app.get("/subscribers/count")
def subscriber_count():
    db = next(get_db())
    count = db.query(Subscriber).filter_by(is_active=True).count()
    return {"active_subscribers": count}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))