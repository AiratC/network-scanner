import asyncpg



# Глобальная переменная где будет храниться пул соединений
pool = None

async def init_db():
   global pool
   pool = await asyncpg.create_pool(process.env.DATABASE_URL)
   
async def close_db():
   global pool
   if pool:
      await pool.close()


