from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Robot

#机器人状态类型站点动态筛选
#增加机器人crud执行代码
async def create_robot(
        db:AsyncSession,
        robot_date:dict
   ):
    new_robot=Robot(**robot_date)
    db.add(new_robot)
    await db.commit()
    await db.refresh(new_robot)
    return new_robot

#查单台机器人详细接口
async def get_robot_by_id(
        db:AsyncSession,
        robot_id:int
):
    stmt=select(Robot).where(Robot.id==robot_id)
    result=await db.execute(stmt)
    return result.scalar_one_or_none()
#查重
async def get_robot_by_name(
        db:AsyncSession,
        name:str
):
    query=select(Robot).where(Robot.name==name)
    result=await db.execute(query)
    return result.scalar_one_or_none()


#查看机器人列表
async def get_robots_list(
    db:AsyncSession,
    status:str|None=None,
    robot_type:str|None=None,
    site_id:int|None=None
):
    #查询语句
    stmt=select(Robot)
    #动态拼接where条件
    if status:
        stmt=stmt.where(Robot.status==status)
    if robot_type:
        stmt=stmt.where(Robot.robot_type==robot_type)
    if site_id:
        stmt=stmt.where(Robot.site_id==site_id)
    #数据库执行查询结果
    result=await db.execute(stmt)
    return result.scalars().all()

#crud机器人改状态或信息
async def update_robot(
        db:AsyncSession,
        db_robot:Robot,
        update_data:dict #更新数据
):
    for key,value in update_data.items():
        setattr(db_robot,key,value)

    await db.commit()
    await db.refresh(db_robot)
    return db_robot

#删除机器人
async def delete_robot(
        db:AsyncSession,
        db_robot:Robot
):
    await db.delete(db_robot)
    await db.commit()
    return True
