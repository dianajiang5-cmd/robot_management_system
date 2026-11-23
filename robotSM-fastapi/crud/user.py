from sqlalchemy import select
import asyncio
from models import User
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.user import UserCreate
import secrets
from redis.asyncio import Redis
from security import pwd_context,get_hash_password
from typing import cast


#根据用户名查询数据库里是否存在
async def get_user_by_username(db:AsyncSession,username:str):
    query=select(User).where(User.username==username)
    result=await db.execute(query)
    return result.scalar_one_or_none()

#创建用户
async def create_user(db:AsyncSession,user_in:UserCreate,hashed_password:str):
    #crud只负责把数据存数据库里，密码加密是router交给crud之前就该做好的
    user=User(
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_password,
        role_name=user_in.role_name,
        is_active=user_in.is_active
        )
    #用户信息传入数据库
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user

#用户登录时信息验证
async def  authenticate_user(db:AsyncSession,username:str,password:str):
    user=await get_user_by_username(db,username)
    if not user:
        return None
    user=cast(User,user)
    #bcrypt是cpu密集操作，丢在线程池里避免阻塞
    is_password_correct = await asyncio.to_thread(pwd_context.verify, password, user.hashed_password)# type: ignore
    if not is_password_correct:
        return None
    if not user.is_active:
        return None
    return user

# 生成token函数
TOKEN_EXPIRE_SECONDS=7*24*60*60
def token_key(token:str):
    return f'auth:token:{token}'

def user_token_key(user_id:int):
    return f'auth:user_token:{user_id}'

#生成token并写入redis7天过期，同一用户重复登录时旧token会被主动失效
async def create_token(redis:Redis,user_id:int):
    # 1查用户是否有token有旧删除旧的
    old_token=await redis.get(user_token_key(user_id))
    if old_token:
        await redis.delete(token_key(str(old_token)))

    #2生成新的token32字节随机数URL安全
    token=secrets.token_urlsafe(32)

    #3pipeline保证两条写入的原子性
    pipe=redis.pipeline()
    pipe.set(token_key(token),str(user_id),ex=TOKEN_EXPIRE_SECONDS)  # noqa
    pipe.set(user_token_key(user_id),token,ex=TOKEN_EXPIRE_SECONDS)  # noqa
    await pipe.execute()
    return token

#鉴权根据token拿到user_id
async def get_user_id_by_token(redis:Redis,token:str):
    uid=await redis.get(token_key(token))
    return int(uid) if uid else None

#根据id查用户
async def get_user_by_id(db:AsyncSession,user_id:int):
    query=select(User).where(User.id==user_id)
    result=await db.execute(query)
    return result.scalar_one_or_none()

#修改用户密码接口
#代码思路：先校验旧密码然后在生成新哈希密码最后存进数据库
async def change_password(db:AsyncSession,user:User,old_password:str,new_password:str):
    #1.用pwd_context.verify 校验旧密码
    if not pwd_context.verify(old_password,user.hashed_password):
        return False
    #2.用get_hash_password 生成新哈希
    hashed_new_pwd=get_hash_password(new_password)
    user.hashed_password=hashed_new_pwd

    await db.commit()
    await db.refresh(user)
    return True

#退出登录删除token
async def delete_token(redis:Redis,token:str,user_id:int):
    pipe=redis.pipeline()
    pipe.delete(token_key(token)) # noqa
    pipe.delete(user_token_key(user_id)) # noqa
    await pipe.execute()

#删除用户
async def delete_user_by_id(db:AsyncSession,user_id:int):
    #先检查用户存在不存在
    user=await get_user_by_id(db,user_id)
    if not user:
        return False

    await db.delete(user)
    await db.commit()
    return True






