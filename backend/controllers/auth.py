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
      httponly=True,     # Защита от XSS (JS на фронтенде не сможет её украсть)
      max_age=604800, # У тебя токен живет 7 дней, давай и куку сделаем на 7 дней (3600 * 24 * 7)
      samesite="lax",    # Защита от CSRF
      secure=False,      # Для разработки на localhost оставляем False
   )
   
   # 5. Возвращаем JSON с данными пользователя для Redux-стейта
   return {
      "email": user["email"],
      "name": user["name"]
   }