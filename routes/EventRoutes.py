from fastapi import Body, APIRouter, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import datetime

from models.EventModel import EventModel


router = APIRouter()

@router.post("/mintticket", response_description="Log mint ticket event", response_model=EventModel)
async def log_event(request: Request, event: EventModel):
    event = jsonable_encoder(event)
    ###
    '''
    Body : {
        contract_id, to_wallet_id, ticket_id, data {value, gas_fees}
    }
    '''
    event["timestamp"] = datetime.datetime.now().isoformat()
    event["type"] = "mint"
    event["from_wallet_id"] = "" # First owner of the ticket
    ###
    new_event = request.app.collection.insert_one(event)
    created_event = request.app.collection.find_one({"_id": new_event.inserted_id})
    return JSONResponse(status_code=status.HTTP_200_OK, content=created_event)

@router.post("/transferticket", response_description="Log transfer ticket in secondary market event", response_model=EventModel)
async def log_event(request: Request, event: EventModel):
    event = jsonable_encoder(event)
    ###
    '''
    Body : {
        contract_id, from_wallet_id, to_wallet_id, ticket_id, data {value, gas_fees}
    }
    '''
    event["timestamp"] = datetime.datetime.now().isoformat()
    event["type"] = "transfer"
    ###
    new_event = request.app.collection.insert_one(event)
    created_event = request.app.collection.find_one({"_id": new_event.inserted_id})
    return JSONResponse(status_code=status.HTTP_200_OK, content=created_event)

# @router.post("/sellticket", response_description="Log sell ticket to secondary market event", response_model=EventModel)
# async def log_event(request: Request, event: EventModel):
#     event = jsonable_encoder(event)
#     ###
#     '''
#     Body : {
#         contract_id, from_wallet_id, to_wallet_id, ticket_id, data {value, gas_fees}
#     }
#     '''
#     event["timestamp"] = datetime.datetime.now().isoformat()
#     event["type"] = "sell"
#     ###
#     new_event = request.app.collection.insert_one(event)
#     created_event = request.app.collection.find_one({"_id": new_event.inserted_id})
#     return JSONResponse(status_code=status.HTTP_200_OK, content=created_event)

@router.post("/onsaleticket", response_description="Log on sale ticket event", response_model=EventModel)
async def log_event(request: Request, event: EventModel):
    event = jsonable_encoder(event)
    ###
    '''
    Body : {
        contract_id, from_wallet_id, ticket_id, data {gas_fees}
    }
    '''
    event["timestamp"] = datetime.datetime.now().isoformat()
    event["type"] = "onsale"
    event["to_wallet_id"] = event["from_wallet_id"] # No ticket exchange
    ###
    new_event = request.app.collection.insert_one(event)
    created_event = request.app.collection.find_one({"_id": new_event.inserted_id})
    return JSONResponse(status_code=status.HTTP_200_OK, content=created_event)

@router.post("/offsaleticket", response_description="Log off sale ticket event", response_model=EventModel)
async def log_event(request: Request, event: EventModel):
    event = jsonable_encoder(event)
    ###
    '''
    Body : {
        contract_id, from_wallet_id, ticket_id, data {gas_fees}
    }
    '''
    event["timestamp"] = datetime.datetime.now().isoformat()
    event["type"] = "offsale"
    event["to_wallet_id"] = event["from_wallet_id"] # No ticket exchange
    ###
    new_event = request.app.collection.insert_one(event)
    created_event = request.app.collection.find_one({"_id": new_event.inserted_id})
    return JSONResponse(status_code=status.HTTP_200_OK, content=created_event)