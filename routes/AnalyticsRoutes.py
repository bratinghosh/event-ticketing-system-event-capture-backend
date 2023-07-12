from calendar import TUESDAY
from fastapi import Body, APIRouter, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import datetime

# from models.EventModel import EventModel
from models.AnalyticsModel import AnalyticsModel

router = APIRouter()

####################################################################################
# MINT ANALYTICS
####################################################################################

@router.get("/mint/totalticketsminted", response_description="Total tickets minted", response_model=AnalyticsModel)
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

@router.get("/mint/totalticketsmintedtoday", response_description="Total tickets minted today", response_model=AnalyticsModel)
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

@router.get("/mint/totalticketsmintedbyweekdays", response_description="Total tickets minted by weekdays", response_model=AnalyticsModel)
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

@router.get("/mint/totalticketsmintedbyday", response_description="Total tickets minted by day", response_model=AnalyticsModel)
async def log_event(request: Request):
    events = request.app.collection.find({"type": "mint"})
    events = [event for event in events]

    totalticketsmintedbyday = {}
    for event in events:
        timestamp = datetime.datetime.fromisoformat(event["timestamp"])
        date = str(timestamp.date())
        if date in totalticketsmintedbyday.keys():
            totalticketsmintedbyday[date] += 1
        else:
            totalticketsmintedbyday[date] = 1
    
    days = []
    totalmints = []

    for key in sorted(totalticketsmintedbyday.keys()):
        days.append(key)
        totalmints.append(totalticketsmintedbyday[key])

    analytics = {
        "data": {
            "days": days,
            "totalticketsmintedbyday": totalmints
        }
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=analytics)

@router.get("/mint/cumulativeticketsmintedbyday", response_description="Cumulative tickets minted by day", response_model=AnalyticsModel)
async def log_event(request: Request):
    events = request.app.collection.find({"type": "mint"})
    events = [event for event in events]

    totalticketsmintedbyday = {}
    for event in events:
        timestamp = datetime.datetime.fromisoformat(event["timestamp"])
        date = str(timestamp.date())
        if date in totalticketsmintedbyday.keys():
            totalticketsmintedbyday[date] += 1
        else:
            totalticketsmintedbyday[date] = 1
    
    days = []
    totalmints = []

    for key in sorted(totalticketsmintedbyday.keys()):
        days.append(key)
        totalmints.append(totalticketsmintedbyday[key])
    
    v = 0
    cumulativeticketsmintedbyday = [v := v + n for n in totalmints]

    analytics = {
        "data": {
            "days": days,
            "cumulativeticketsmintedbyday": cumulativeticketsmintedbyday
        }
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=analytics)

####################################################################################
# USER ANALYTICS
####################################################################################
@router.get("/user/ticketsperuserfrequency", response_description="Frequncy of Tickets held per user", response_model=AnalyticsModel)
async def log_event(request: Request):
    ticketsperuser = {}

    events = request.app.collection.find({"type": "mint"})
    events = [event for event in events]

    for event in events:
        user = event["to_wallet_id"]
        if user in ticketsperuser.keys():
            ticketsperuser[user] += 1
        else:
            ticketsperuser[user] = 1
    
    events = request.app.collection.find({"type": "transfer"})
    events = [event for event in events]

    for event in events:
        old_user = event["from_wallet_id"]
        if old_user in ticketsperuser.keys():
            ticketsperuser[old_user] -= 1

        new_user = event["to_wallet_id"]
        if new_user in ticketsperuser.keys():
            ticketsperuser[new_user] += 1
        else:
            ticketsperuser[new_user] = 1

    ticketsperuserfrequency = {}

    for _, tickets in ticketsperuser.items():
        key = "9+" if tickets > 9 else str(tickets)
        if key in ticketsperuserfrequency.keys():
            ticketsperuserfrequency[key] += 1
        else:
            ticketsperuserfrequency[key] = 1

    ticketscount = []
    frequency = []

    for key in sorted(ticketsperuserfrequency.keys()):
        ticketscount.append(key)
        frequency.append(ticketsperuserfrequency[key])

    analytics = {
        "data": {
            "ticketscount": ticketscount,
            "frequency": frequency
        }
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=analytics)

####################################################################################
# SECONDARY MARKET ANALYTICS
####################################################################################