
from fastapi import APIRouter
from fastapi.responses import  JSONResponse
from pydantic import BaseModel
from utils.jwt_manager import create_token
from schemas.user import User

user_router = APIRouter()



@user_router.post("/login", tags=["auth"])
def login(user:User):
    if user.email == "johan@gmail.com" and user.password == "johan":
        token:str = create_token(user.dict())
        return JSONResponse(status_code=200, content=token)
    return User