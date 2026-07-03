from fastapi import APIRouter, Response, Depends
from schemas.auth import LoginRequest, UserResponse
from controllers.auth_controller import handle_login, handle_logout
from utils.dependencies import get_current_user

auth_router = APIRouter(
   prefix="/auth",
   tags=["Auth"]
)

@auth_router.post("/login", response_model=UserResponse)
async def login(credentials: LoginRequest, response: Response):
   print(credentials)
   return await handle_login(credentials, response)

@auth_router.get("/get-me", response_model=UserResponse)
async def get_me(current_user = Depends(get_current_user)):
   print('get-me router')
   """
   Эндпоинт возвращает данные текущего вошедшего пользователя.
   Сюда невозможно попасть, если кука пустая или токен «протух» —
   зависимость get_current_user отсечет запрос раньше.
   """
   # current_user — это то, что вернула функция get_current_user (запись из БД)
   return {
      "email": current_user["email"],
      "name": current_user["name"]
   }
   
@auth_router.post("/logout")
async def logout(response: Response):
   return await handle_logout(response)