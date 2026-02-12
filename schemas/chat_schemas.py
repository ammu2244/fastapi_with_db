from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ChatRequest(BaseModel):
    message: str


class ChatMessageResponse(BaseModel):
    id: int
    user_email: str
    role: str
    message: str
    timestamp: datetime

    class Config:
        from_attributes = True


class ChatResponse(BaseModel):
    response: str
