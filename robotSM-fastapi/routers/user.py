from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security import OAuth2PasswordRequestForm

from cache.cache_config import redis_client
from database import get_db
from dependencies import get_current_user,RoleChecker
from schemas.user import UserResponse, UserCreate, TokenResponse, UserChangePasswordRequest

from crud import user
from security import pwd_context
from models import User,UserRole
from response import success_response
from crud import user as crud_user


router = APIRouter(prefix="/api/user", tags=["用户管理"])
allow_delete_user=RoleChecker([UserRole.ADMIN,UserRole.EDITOR])

#用户注册接口思路：1.接口先去crud数据库查询用户是否是否存在，2.接口调用crud里面的创建功能，
#3.crud按照model里user模型类信息创建用户信息,存入数据库，然后接口在返回给前端

#用户注册接口功能代码
@router.post("/register",response_model=UserResponse)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
     #调用crud检查用户函数是否存在
     existing_user=await user.get_user_by_username(db, user_in.username)
     #如果用户已存在抛异常
     if existing_user:
         raise HTTPException(status_code=400,detail='用户名已存在')
     #没有异常router加密密码
     hashed_pwd = pwd_context.hash(user_in.password)
     #然后告诉crud把用户加入数据库
     new_user = await user.create_user (db, user_in, hashed_pwd)
     #crud存好数据，router返回前端
     return new_user

#用户登录接口功能
#登录功能逻辑：验证用户是否存在-验证哈希密码成功后-生成token存入redis7天过期-返回token给前端
@router.post("/login",response_model=TokenResponse)
async def login(
     form: OAuth2PasswordRequestForm = Depends(),
     db:AsyncSession=Depends(get_db),
):
     db_user=await user.authenticate_user(db, form.username, form.password)
     #统一错误信息响应
     if not db_user:
          raise HTTPException(
               status_code=status.HTTP_401_UNAUTHORIZED,
               detail='Incorrect username or password',
          )
     #生成token存入redis
     token=await user.create_token(redis_client, db_user.id)

     return TokenResponse(
          access_token=token,
           token_type="bearer",
          expires_in=user.TOKEN_EXPIRE_SECONDS,
     )
#获取信息用户接口
#思路是：定义函数然后调dependencies里的get_current_user函数来校验用户
#校验成功后然后返回schema里的UserResponse函数
@router.get("/info",response_model=UserResponse)
async def get_user_info(current_user:User=Depends(get_current_user)):
     return current_user

#修改密码接口
#代码思路：调dependencies校验用户函数-调用crud里更改密码函数-调用schemas更改密码函数
@router.put("/password")
async def update_password(
     password_data:UserChangePasswordRequest,
     current_user:User=Depends(get_current_user),
     db:AsyncSession=Depends(get_db),
):
     #调用crud的change_password函数
     res_change_pwd=await user.change_password(db, current_user, password_data.old_password, password_data.new_password)
     if not res_change_pwd:
          raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail='修改密码失败')
     return success_response ('修改密码成功')

#删除用户
@router.delete("/{user_id}")
async def delete_user(
     user_id:int,
     db:AsyncSession=Depends(get_db),
     _current_user=Depends(allow_delete_user),
):
     #安全校验管理员不能自己删除自己
     if not _current_user.id==user_id:
          raise HTTPException(status_code=400,detail='管理员不能删除自己的账号')
     #调用crud删除
     id_deleted=await crud_user.delete_user_by_id(db, user_id)
     if not id_deleted:
          raise HTTPException(status_code=404,detail='该用户不存在')
     return success_response('用户删除成功')


