import os
from dotenv import load_dotenv
from fastapi import FastAPI, Body, HTTPException, status, Request
from fastapi.responses import Response, JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pymongo import MongoClient
# from pymongo.server_api import ServerApi
import certifi

from models.EventModel import EventModel
from routes.EventRoutes import router as EventRouter
from routes.AnalyticsRoutes import router as AnalyticsRouter


load_dotenv()

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://localhost:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(os.environ["DATABASE_URL"], tlsCAFile=certifi.where())
    app.database = app.mongodb_client["test"]
    app.collection = app.database["events"]

    # Send a ping to confirm a successful connection
    try:
        app.mongodb_client.admin.command('ping')
        print("You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(EventRouter, tags=["Event"], prefix="/events")
app.include_router(AnalyticsRouter, tags=["Analytics"], prefix="/analytics")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ["PORT"]))

