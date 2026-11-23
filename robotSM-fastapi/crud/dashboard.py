from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func
from models import Robot,Alert,RobotParameter

async def get_dashboard_stats(db:AsyncSession)->dict:
    #1机器人总数
    total_robots_res=await db.execute(select(func.count(Robot.id)))
    total_robots=total_robots_res.scalar() or 0

    #2在线数量status不是offline就是在线
    online_res=await db.execute(select(func.count(Robot.id)).where(Robot.status !='offline'))
    online_robots=online_res.scalar() or 0

    #3机器人在线率
    online_rate_val=(online_robots/total_robots *100) if total_robots >0 else 0
    online_rate=f'{online_rate_val:.1f}%'

    #4告警数量,未解决的告警
    alert_res=await db.execute(select(func.count(Alert.id)).where(Alert.is_resolved==False))
    active_alerts=alert_res.scalar() or 0

    #5异常参数比例，参数数量/总参数量
    total_params_res=await db.execute(select(func.count(RobotParameter.id)))
    total_params=total_params_res.scalar() or 0

    abnormal_params_res=await db.execute(select(func.count(RobotParameter.id)).where(RobotParameter.is_abnormal==True))
    abnormal_params=abnormal_params_res.scalar() or 0

    abnormal_rate_val=(abnormal_params/total_params *100) if total_params>0 else 0
    abnormal_param_rate=f"{abnormal_rate_val:.1f}%"

    #6状态分布，按照一列或多列值分
    status_res=await db.execute(
        select(Robot.status,func.count(Robot.id)).group_by(Robot.status)
    )
    #将status和count转换成字典
    status_distribution={row[0]:row[1] for row in status_res.all()}
    return {
        "total_robots":total_robots,
        "online_robots":online_robots,
        "online_rate":online_rate,
        "active_alerts":active_alerts,
        "abnormal_params_rate":abnormal_param_rate,
        "status_distribution":status_distribution
    }




