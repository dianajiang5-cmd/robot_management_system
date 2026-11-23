from sqlalchemy.ext.asyncio import AsyncSession
from models import RobotParameter,Alert

#判断异常”和“自动生成告警”的联动逻辑
async def create_parameter_and_chek_alert(
        db:AsyncSession,
        robot_id:int,
        param_data:dict
):
    #1判断是否超出阈值
    is_abnormal=False
    if param_data['value']<param_data['min_threshold'] or param_data['value']>param_data['max_threshold']:
        is_abnormal=True

    #2写入参数记录
    new_param=RobotParameter(
        robot_id=robot_id,
        is_abnormal=is_abnormal,
        **param_data
    )
    db.add(new_param)

    #3如果异常 就会自动生成告警
    if is_abnormal:
        alert_msg=(f"机器人({robot_id})参数异常:{param_data['name']}当前值为{param_data['value']} {param_data['unit']}"
                   f",超出安全范围[{param_data['min_threshold']}~{param_data['max_threshold']}]")
        new_alert=Alert(
            robot_id=robot_id,
            message=alert_msg,
            level='error'
        )
        db.add(new_alert)
    await db.commit()
    await db.refresh(new_param)
    return new_param



