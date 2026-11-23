from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database  import get_db
from schemas.monitor import ParamUpload,ParamResponse
from crud.monitor import create_parameter_and_chek_alert
from crud.robot import get_robot_by_id
from cache.cache_config import set_cache


router=APIRouter(prefix="/api/monitor",tags=["机器人参数监控"])

#这里把机器人参数数据写入数据库后，立刻把它更新到 Redis，方便前端仪表盘立刻读取
@router.post("/robot/{robot_id}/param",response_model=ParamResponse)
async def upload_robot_param(
        robot_id: int,
        param_in: ParamUpload,
        db:AsyncSession = Depends(get_db),
):
    #1先检查机器人是否存在
    robot=await get_robot_by_id(db,robot_id)
    if not robot:
        raise HTTPException(status_code=404,detail='该机器人不存在')
    #2数据库入库并检查是否自动生成告警
    new_param=await create_parameter_and_chek_alert(db,robot_id,param_in.model_dump())

    #3写入redis缓存调用cache里面的set_cache函数转json
    cache_key=f"robot:param:{robot_id}:{param_in.name}"
    #因为set_cache函数执行json.dumps所以时间必须转字符串不能传datetime
    cache_data={
        'value': param_in.value,
        'unit': param_in.unit,
        'is_abnormal': new_param.is_abnormal,
        'time': new_param.created_at.strftime("%Y-%m-%d %H:%M:%S")
    }
    #传入字典设置3600秒后过期
    await set_cache(cache_key,cache_data,expire=3600)
    return new_param








