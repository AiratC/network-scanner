from fastapi import HTTPException, Response
from utils import database
from utils.security import verify_password
from utils.jwt import create_access_token
from schemas.auth import LoginRequest
from repositories.auth_repository import AuthRepository

async def handle_login(credentials: LoginRequest, response: Response):
   # Ищем пользователя в БД
   user = await AuthRepository.get_user_by_email(credentials.email)
   
   # 2. Если не нашли или хэш пароля не совпал — отдаем 401
   if not user or not verify_password(credentials.password, user["hashed_password"]):
      raise HTTPException(status_code=401, detail="Неверный email или пароль")
   
   # 3. Генерируем JWT
   token_data = { "user_id": user["id"], "email": user["email"] }
   token = create_access_token(token_data)
   
   # 4. Сажаем JWT в безопасную HttpOnly куку
   response.set_cookie(
    key="access_token",
    value=token,
    httponly=True,     # Защита от XSS (JS не сможет украсть токен)
    max_age=604800,    # 7 дней в секундах
    samesite="lax",    # Позволяет браузеру передавать куку при cross-origin запросах на localhost
    secure=False,      # ОБЯЗАТЕЛЬНО False. Если поставить True, кука работает ТОЛЬКО по HTTPS. На localhost у нас HTTP, поэтому True её полностью блокирует!
    path="/",          # ОБЯЗАТЕЛЬНО. Говорит браузеру: кука доступна для ВСЕХ эндпоинтов бэкенда, начиная с корня
)
   
   # 5. Возвращаем JSON с данными пользователя для Redux-стейта
   return {
      "email": user["email"],
      "name": user["name"]
   }
   
async def handle_logout(response: Response):
   """Удаляет HttpOnly куку авторизации из браузера"""
   response.delete_cookie(
      key="access_token",
      httponly=True,
      samesite="lax",
      secure=False # Должно совпадать с настройками при set_cookie
   )
   return {"detail": "Успешный выход из системы"}