import traceback
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from models import MaintenanceRecord


#维修记录crud
#新增维修记录
async def create_maintenance(
        db:AsyncSession,
        data:dict,
        user_id:int
):
    try:
        record=MaintenanceRecord(**data,performer_id=user_id)
        db.add(record)
        await db.commit()
        await db.refresh(record)
        return record

    except Exception as e:
    # 强行将完整的报错栈打印到终端
        print("========= 数据库插入报错 =========")
        traceback.print_exc()
        print("==================================")
        raise e

#查看维修列表
async def get_maintenance_list(
        db:AsyncSession,
        robot_id:int|None=None
):
    stmt=select(MaintenanceRecord)
    if robot_id:
        stmt=stmt.where(MaintenanceRecord.robot_id==robot_id)
    stmt=stmt.order_by(MaintenanceRecord.created_date.desc())
    result=await db.execute(stmt)
    return result.scalars().all()

#统计维修费用和总周期
async def get_maintenance_cost_duration(
        db:AsyncSession,
):
    stmt=select(
        func.sum(MaintenanceRecord.cost).label('total_cost'),
        func.sum(MaintenanceRecord.duration).label('total_duration'),
        func.count(MaintenanceRecord.id).label('total_count')
    )
    result=await db.execute(stmt)
    row=result.first()

    if not row or row.total_cost is None:
        return {
            "total_cost": 0.0,
            "total_duration": 0,
            "total_count": 0
        }
    return {
        "total_cost": round(row.total_cost, 2),  # 顺便保留两位小数，防止浮点数出现 399.800000001
        "total_duration": row.total_duration or 0,
        "total_count": row.total_count or 0
    }
