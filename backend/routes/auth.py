from fastapi import APIRouter, Response
from schemas.auth import LoginRequest, UserResponse
from controllers.auth import handle_login

auth_router = APIRouter(
   prefix="/auth",
   tags=["Auth"]
)

@auth_router.post("/login", response_model=UserResponse)
async def login(credentials: LoginRequest, response: Response):
   return await handle_login(credentials, response)