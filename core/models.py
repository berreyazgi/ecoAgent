from pydantic import BaseModel
from typing import List, Optional 

class UserProfile(BaseModel):
    name: str
    interests: List[str]
    location: str


class EventData(BaseModel):
    title: str
    description: str
    source_url: str
    trust_score: float 
    category: Optional[str] = None