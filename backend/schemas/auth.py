from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
   email: EmailStr # Строгая валидация почты (email-validator как раз тут и работает)
   password: str
   
class UserResponse(BaseModel):
   email: str
   name: str
   
   class Config:
      from_attributes = True