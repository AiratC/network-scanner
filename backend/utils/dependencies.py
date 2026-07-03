import jwt
from fastapi import Request, HTTPException, Depends
from utils.jwt import SECRET_KEY, ALGORITHM
from repositories.auth_repository import AuthRepository

async def get_current_user(request: Request):
    """
    Зависимость для извлечения текущего пользователя из JWT в HttpOnly куках.
    """
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Вы не авторизованы (токен отсутствует)")
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")
        if not email:
            raise HTTPException(status_code=401, detail="Невалидный токен (отсутствуют данные)")
            
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Срок действия токена истек. Войдите заново")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Невалидный токен авторизации")
    
    user = await AuthRepository.get_user_by_email(email)
    if user is None:
        raise HTTPException(status_code=401, detail="Пользователь не найден в системе")
    
    return user