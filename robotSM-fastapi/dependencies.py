from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from database import get_db
from cache.cache_config import redis_client
from models import User,UserRole
from crud.user import get_user_by_id,get_user_id_by_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/user/login")


#登录校验依赖和权限依赖角色校验，在登录之后
#登录验证，获取当前用户
async def get_current_user(
        token:str=Depends(oauth2_scheme),
        db:AsyncSession=Depends(get_db),
        redis:Redis=Depends(lambda:redis_client),#使用全局redis_client
)->User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='登录已过期或无效凭证，请重新登录',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    #1.从redis中解析user_id
    user_id=await get_user_id_by_token(redis,token)
    if user_id is None:
        raise credentials_exception
    #2.查数据库获取用户
    user=await get_user_by_id(db,user_id)
    if user is None:
        raise credentials_exception
    #3.检查用户是否被禁用
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='该账号已被禁止使用'
        )
    return user


#角色权限验证
class RoleChecker:
    def __init__(self,allowed_roles:list[UserRole]):
        self.allowed_roles=allowed_roles

    def __call__(self,current_user:User=Depends(get_current_user))->User:
        #判断用户的角色是否在允许的列表中
        if current_user.role_name not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='权限不足，您没有执行此操作的权限'
            )
        return current_user


