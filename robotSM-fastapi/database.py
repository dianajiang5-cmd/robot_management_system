import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from models import Base

#获取当前文件db所在的绝对目录
BASE_DIR=os.path.dirname(os.path.abspath(__file__))
DB_PATH=os.path.join(BASE_DIR, 'robotSM.db')


#1.sqlite数据库异步连接URL路径
ASYNC_DATABASE_URL=f'sqlite+aiosqlite:///{DB_PATH}'

#2.创建异步引擎
async_engine=create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True, #查看SQL
)
#3.异步会话工厂
AsyncSessionLocal=async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

#4.依赖函数：接口里获取数据库会话db session
async def get_db():
    async with AsyncSessionLocal() as session:
       try:
           yield session
           await session.commit()
       except Exception:
           await session.rollback()
           raise
       finally:
           await session.close()

#5.建表函数main.py启动时调用一次
async def create_db_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('数据库表结构创建完毕')

