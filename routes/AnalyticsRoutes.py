from calendar import TUESDAY
from fastapi import Body, APIRouter, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import datetime

# from models.EventModel import EventModel
from models.AnalyticsModel import AnalyticsModel

router = APIRouter()

@router.get("/totalticketsminted", response_description="Total tickets minted", response_model=AnalyticsModel)
async def log_event(request: Request):
    events = request.app.collection.find({"type": "mint"})
    events = [event for event in events]

    totalticketsminted = len(events)

    analytics = {
        "data": {
            "totalticketsminted": totalticketsminted
        }
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=analytics)

@router.get("/totalticketsmintedtoday", response_description="Total tickets minted today", response_model=AnalyticsModel)
async def log_event(request: Request):
    events = request.app.collection.find({"type": "mint"})
    events = [event for event in events]

    totalticketsmintedtoday = 0
    for event in events:
        timestamp = datetime.datetime.fromisoformat(event["timestamp"])
        if datetime.datetime.now().weekday() == timestamp.weekday():
            totalticketsmintedtoday += 1
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    analytics = {
        "data": {
            "weekday": weekdays[datetime.datetime.now().weekday()],
            "totalticketsmintedtoday": totalticketsmintedtoday
        }
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=analytics)

@router.get("/totalticketsmintedbyweekdays", response_description="Total tickets minted by weekdays", response_model=AnalyticsModel)
async def log_event(request: Request):
    events = request.app.collection.find({"type": "mint"})
    events = [event for event in events]

    totalticketsmintedbyweekdays = [0, 0, 0, 0, 0, 0]
    for event in events:
        timestamp = datetime.datetime.fromisoformat(event["timestamp"])
        totalticketsmintedbyweekdays[timestamp.weekday()] += 1

    analytics = {
        "data": {
            "weekdays": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "totalticketsmintedbyweekdays": totalticketsmintedbyweekdays
        }
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=analytics)