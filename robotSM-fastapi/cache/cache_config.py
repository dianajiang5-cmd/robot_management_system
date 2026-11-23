import redis.asyncio as redis
import json
from typing import Any


REDIS_HOST='127.0.0.1'
REDIS_PORT=6379
REDIS_DB=0

#创建Redis连接对象
redis_client=redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,#redis数据库编号0-15
    decode_responses=True#是否将字节数据解码为字符串
)
#设置缓存和读取，字符串和列表或字典
#读取字符串缓存
async def get_cache(key:str):
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f'获取缓存失败：{e}')
        return None
#读取列表和字典缓存
async def get_json(key:str):
    try:
        data=await redis_client.get(key)
        if data:
            return json.loads(data)#序列化
        return None
    except Exception as e:
        print(f'获取JSON缓存失败{e}')
        return None
#设置封装缓存key,expire,value
async def set_cache(key:str,value:Any,expire:int=3600):
    try:
        if isinstance(value,(dict,list)):
            #转字符串存入
            value=json.dumps(value,ensure_ascii=False)#中文正常保持
        await redis_client.setex(key,expire,value)
        return True
    except Exception as e:
        print(f'设置缓存失败:{e}')
        return False
#删除token
async def delete_cache(key:str):
    try:
        await redis_client.delete(key)
    except Exception as e:
        print(f'删除缓存失败：{e}')

#timeToLive存货时间/过期倒计时，
async def get_ttl(key:str):
    try:
        return await redis_client.ttl(key)
    except Exception as e:
        print(f'获取TTL失败:{e}')
        return -2




