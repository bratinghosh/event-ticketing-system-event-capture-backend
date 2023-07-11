from pydantic import BaseModel
from typing import Dict, Optional

class AnalyticsModel(BaseModel):
    data: Dict