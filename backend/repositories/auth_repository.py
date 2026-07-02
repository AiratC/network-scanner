from utils import database

class AuthRepository:
   @staticmethod
   async def get_user_by_email(email: str):
      """Достает пользователя из БД по его email"""
      return await database.pool.fetchrow(
         "SELECT id, email, hashed_password, name FROM users WHERE email = $1",
         email
      )