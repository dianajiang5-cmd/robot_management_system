from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#使用哈希密码保护，明文改暗文
def get_hash_password(password:str):
    return pwd_context.hash(password)