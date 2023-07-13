from calendar import TUESDAY
from fastapi import Body, APIRouter, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import datetime

# from models.EventModel import EventModel
from models.AnalyticsModel import AnalyticsModel

router = APIRouter()

@router.get("", response_description="Analytics", response_model=AnalyticsModel)
async def log_event(request: Request):
    analytics = {
        "data": {
            "totalticketsminted": totalticketsminted(request),
            "totalticketsmintedtoday": totalticketsmintedtoday(request),
            "totalticketsmintedbyweekdays": totalticketsmintedbyweekdays(request),
            "totalticketsmintedbyday": totalticketsmintedbyday(request),
            "cumulativeticketsmintedbyday": cumulativeticketsmintedbyday(request),
            "ticketsperuserfrequency": ticketsperuserfrequency(request),
            "ticketsonsale": ticketsonsale(request),
        }
    }
    return JSONResponse(status_code=status.HTTP_200_OK, content=analytics)

####################################################################################
# MINT ANALYTICS
####################################################################################

def totalticketsminted(request: Request):
    events = request.app.collection.find({"type": "mint"})
    events = [event for event in events]

    totalticketsminted = len(events)

    analytics = {
        "data": {
            "totalticketsminted": totalticketsminted
        }
    }
    return analytics

def totalticketsmintedtoday(request: Request):
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
    return analytics

def totalticketsmintedbyweekdays(request: Request):
    events = request.app.collection.find({"type": "mint"})
    events = [event for event in events]

    totalticketsmintedbyweekdays = [0, 0, 0, 0, 0, 0, 0]
    for event in events:
        timestamp = datetime.datetime.fromisoformat(event["timestamp"])
        totalticketsmintedbyweekdays[timestamp.weekday()] += 1

    analytics = {
        "data": {
            "weekdays": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
            "totalticketsmintedbyweekdays": totalticketsmintedbyweekdays
        }
    }
    return analytics

def totalticketsmintedbyday(request: Request):
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
    return analytics

def cumulativeticketsmintedbyday(request: Request):
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
    return analytics

####################################################################################
# GENERAL ANALYTICS
####################################################################################

def ticketsperuserfrequency(request: Request):
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
    return analytics

####################################################################################
# SECONDARY MARKET ANALYTICS
####################################################################################
def ticketsonsale(request: Request):
    events = request.app.collection.find({"type": "onsale"})
    events = [event for event in events]

    tickets = []

    for event in events:
        ticket_id = event["ticket_id"]
        tickets.append(ticket_id)

    events = request.app.collection.find({"type": "offsale"})
    events = [event for event in events]

    for event in events:
        ticket_id = event["ticket_id"]
        if ticket_id in tickets:
            tickets.remove(ticket_id)
    
    ticketsonsale = len(tickets)
    
    events = request.app.collection.find({"type": "mint"})
    events = [event for event in events]

    totalticketsminted = len(events)

    analytics = {
        "data": {
            "labels": ["On-Sale", "not On-Sale"],
            "ticketsonsale": [ticketsonsale, (totalticketsminted-ticketsonsale)]
        }
    }
    return analytics