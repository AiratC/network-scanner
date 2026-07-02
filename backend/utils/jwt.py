import jwt
from datetime import datetime, timedelta, timezone

SECRET_KEY = "KJBcklbcx6298hGde5gf08g4tfsl"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 10080 # Токен активен (60 * 24) * 7 = 10080;  7 дней

def create_access_token(data: dict) -> str:
   """Генерирует JWT токен с ограниченным сроком действия"""
   # В Python словари передаются по ссылке. Если мы изменим data напрямую, 
   # мы случайно изменим объект в контроллере. .copy() защищает нас от этого эффекта.
   to_encode = data.copy()
   
   # Работа с таймзонами: datetime.now(timezone.utc) — это стандарт для бэкенда,
   # чтобы сервер не путал время, если он задеплоен, например, в другом полушарии.
   expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
   to_encode.update({ "exp": expire })
   
   encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
   return encode_jwt

