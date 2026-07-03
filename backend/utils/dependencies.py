import jwt
from fastapi import Request, HTTPException, Depends
from utils.jwt import SECRET_KEY, ALGORITHM
from repositories.auth_repository import AuthRepository

async def get_current_user(request: Request):
   """
   Зависимость для извлечения текущего пользователя из JWT в HttpOnly куках.
   Если токен невалиден или отсутствует — сразу прерывает запрос ошибкой 401.
   """
   print('get_current_user FN')
   # 1. Достаем куку с именем access_token
   token = request.cookies.get("assess_token")
   print(token)
   
   if not token:
      raise HTTPException(status_code=401, detail="Вы не авторизованы (токен отсутствует)")
   
   try:
      # 2. Декодируем (расшифровываем) JWT токен
      payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
      
      # Извлекаем email (помним, что мы упаковывали его в payload как 'sub' или 'email')
      email: str = payload.get("email")
      if email is None:
         raise HTTPException(status_code=401, detail="Невалидный токен (отсутствуют данные)")
      
   except jwt.ExpiredSignatureError:
      raise HTTPException(status_code=401, detail="Срок действия токена истек. Войдите заново")
   except jwt.InvalidTokenError:
      raise HTTPException(status_code=401, detail="Невалидный токен авторизации")
   
   # 3. Идем в базу через репозиторий и ищем пользователя
   user = await AuthRepository.get_user_by_email(email)
   if user is None:
      raise HTTPException(status_code=401, detail="Пользователь не найден в системе")
   
   # 4. Возвращаем объект пользователя. FastAPI передаст его прямо в эндпоинт!
   return user