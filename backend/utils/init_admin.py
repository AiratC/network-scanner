from utils import database
from utils.security import hash_password

async def init_admin_user():
   """Функция автоматического создания дефолтного админа"""
   # Проверяем, есть ли вообще пользователи в базе
   user_count = await database.pool.fetchval("SELECT COUNT(*) FROM users")
   
   if user_count == 0:
      print("👤 Таблица пользователей пуста. Создаю дефолтного администратора...")
      admin_email = "admin@gmail.com"
      admin_password = "1234567" # Наш учебный секрет
      admin_name = "Admin"
      
      hashed_password = hash_password(admin_password)
      
      await database.pool.execute(
         """
         INSERT INTO users (email, hashed_password, name)
         VALUES ($1, $2, $3)
         """,
         admin_email, hashed_password, admin_name
      )
      print(f"✅ Админ создан! Email: {admin_email} | Пароль: {admin_password}")
   else:
      print("👤 Пользователи уже существуют в БД. Пропускаю создание админа.")