from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from utils.database import init_db, close_db
from routes.scanner_router import scan_router
from routes.auth_router import auth_router
from utils.init_admin import init_admin_user

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    print("База данных успешно подключена (Пул создан)")
    
    # Запускаем создание админа сразу после инициализации пула БД
    await init_admin_user()

    yield
    await close_db()
    print("Подключение к базе данных закрыто")

app = FastAPI(lifespan=lifespan)

# Настройка CORS (что бы фронтенд мог достучаться)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True, 
    allow_methods=["*"], # Разрешаем все методы (GET, POST, PATCH, DELETE)
    allow_headers=["*"], # Разрешаем любые заголовки (включая Authorization)
)

# Регистрируем роутер
app.include_router(scan_router, prefix="/api")
app.include_router(auth_router, prefix="/api")




