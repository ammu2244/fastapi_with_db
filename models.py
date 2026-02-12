from db import Base
from sqlalchemy import Column,Integer,String,DateTime,Text
from datetime import datetime

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    email=Column(String,index=True)
    password=Column(String)


class ChatMessage(Base):
    __tablename__="chat_messages"
    id=Column(Integer,primary_key=True,index=True)
    user_email=Column(String,index=True)
    role=Column(String)  # "user" or "assistant"
    message=Column(Text)
    timestamp=Column(DateTime,default=datetime.utcnow)
