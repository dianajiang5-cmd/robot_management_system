from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from crud import robot as crud_robot
from dependencies import get_current_user,RoleChecker
from schemas.robot import RobotResponse, RobotCreate, RobotUpdate
from models import UserRole
from typing import List

router=APIRouter(prefix="/api/robot",tags=["机器人管理"])
allow_edit = RoleChecker([UserRole.ADMIN, UserRole.EDITOR])

#增加机器人接口
@router.post("/",response_model=RobotResponse)
async def add_robot(
    robot_in:RobotCreate,
    db:AsyncSession=Depends(get_db),
    current_user=Depends(allow_edit) #权限管控，只有编辑者才可以更改机器人状态
):
    #先查重
    existing_robot=await crud_robot.get_robot_by_name(db,robot_in.name)
    if existing_robot:
        raise HTTPException(status_code=400,detail='该机器人名称/编号已存在，请勿重复添加')

    robot_data=robot_in.model_dump()
    robot_data['created_by']=current_user.username
    return await crud_robot.create_robot(db,robot_data)


#查看机器人列表接口，意思是：把符合条件的机器人都给我列出来
@router.get("/get_robot_list",response_model=List[RobotResponse])
async def get_robot(
        status:str|None=None,
        robot_type:str|None=None,
        site_id:int|None=None,
        db:AsyncSession=Depends(get_db),
        _current_user=Depends(get_current_user)#用户必须登录才可以查看信息
):
    #前端/api/robots/?status=working&site_id=1 就能自动过滤
    return await crud_robot.get_robots_list(db,status,robot_type,site_id)

#查看单台机器人的详情信息
@router.get("/{robot_id}",response_model=RobotResponse)
async def get_robot_detail(
        robot_id:int,
        db:AsyncSession=Depends(get_db),
        _current_user=Depends(get_current_user)
):
    robot=await crud_robot.get_robot_by_id(db,robot_id)
    if not robot:
        raise HTTPException(status_code=404,detail='机器人不存在')
    #返回的机器人详情信息会根据schemas里面的RobotResponse参数信息返回
    return robot

#更改机器人信息
@router.put("/{robot_id}",response_model=RobotResponse)
async def update_robot_info(
        robot_id:int,
        robot_in:RobotUpdate,#接收前端传来的新数据
        db:AsyncSession=Depends(get_db),
        _current_user=Depends(allow_edit)
):
    #1先查数据库是否有这台机器人
    db_robot=await crud_robot.get_robot_by_id(db,robot_id)
    if not db_robot:
        raise HTTPException(status_code=404,detail='该机器人不存在')
    #2把前端更新的数据转字典
    update_data=robot_in.model_dump(exclude_unset=True)
    #3调用crud函数
    return await crud_robot.update_robot(db,db_robot, update_data)

#删除机器人
@router.delete("/{robot_id}")
async def delete_robot(
        robot_id:int,
        db:AsyncSession=Depends(get_db),
        _current_user=Depends(allow_edit)
):
    #1先去数据库根据ID找到对应的机器人
    db_robot=await crud_robot.get_robot_by_id(db,robot_id)
    if not db_robot:
        raise HTTPException(status_code=404,detail='该机器人不存在')
    #把查出来的机器人传给crud函数进行删除
    await crud_robot.delete_robot(db,db_robot)
    return {'message':'该机器人成功删除'}

