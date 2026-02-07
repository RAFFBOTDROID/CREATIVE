from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    username: str
    password: str

class Lead(BaseModel):
    name: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    company: Optional[str]
    city: Optional[str]
    niche: Optional[str]
    source: Optional[str]
    status: Optional[str] = "Novo"
    score: Optional[int] = 0
    notes: Optional[str]
