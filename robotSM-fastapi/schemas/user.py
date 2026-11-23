from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import Optional
from models import UserRole
#schemas里面写的是创建用户注册新增时前端提交的数据
#Pydantic,校验前端传过来的参数信息
#用户注册登录相关功能代码，用户按照这里的要求输信息，


#基础模型类信息，所有用户都有的字段放在这里，
class UserBase(BaseModel):
    username:str=Field(...,min_length=3,max_length=20,description='用户名')
    email:EmailStr=Field (...,description='邮箱')#会本Pydantic自动校验格式

#username,email,password是必填
#role_name,is_active是默认值可以不传
class UserCreate(UserBase):
    password:str=Field(...,min_length=6,max_length=15,description='明文密码，服务端会bcrypt加密')
    role_name:Optional[UserRole]=UserRole.VIEWER# type: ignore
    is_active:Optional[bool]=True

#用户登录
class UserLogin(BaseModel):
    username:str=Field(...,min_length=6,max_length=15,description='用户名')
    password:str=Field(...,min_length=6,max_length=15,description='密码')

#返回给前端的响应
class UserResponse(BaseModel):
    id:int
    username:str
    email:EmailStr
    role_name:UserRole
    is_active:bool
    created_at:datetime
    updated_at:datetime

    model_config = ConfigDict(from_attributes=True)

#登录凭证响应
class TokenResponse(BaseModel):
    access_token:str
    token_type:str='bearer'
    expires_in:int#秒

#用户更改密码
class UserChangePasswordRequest(BaseModel):
    old_password:str
    new_password:str

    # 这里 role_name: Optional[UserRole] = None 是允许前端显式传 null 的，
    # 如果你【不允许】把 role 改成 null，就该写成 role_name: UserRole | None = None
    # 然后在 service 里判断 `if data.role_name is not None` 再赋值。



