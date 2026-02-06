from fastapi import APIRouter
from db import get_db
from sqlalchemy.orm import Session
from repositories.user_repo import UserRepo
from fastapi import Depends
from schemas.User_schema import UserSchema

router=APIRouter()

@router.post("/signup")
def signup(db:Session=Depends(get_db),user:UserSchema):
    user_repo=UserRepo(db)
    user_repo.add_user(user)
    return {"message":"User signed up successfully"}
    
@router.post("/login")
def login():
    return {"message":"User logged in successfully"}