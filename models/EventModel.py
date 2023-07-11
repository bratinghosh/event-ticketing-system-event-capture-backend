import uuid
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Dict, Optional

class EventModel(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    contract_id: str
    from_wallet_id:  Optional[str]
    to_wallet_id:  Optional[str]
    ticket_id: str
    # timestamp: datetime
    # type: str
    data: Optional[Dict]

'''
data : {
    value: <price in eth for the transaction>
    gas_fees: <gas fees paid for the transaction>
    .
    .
    .
}
'''