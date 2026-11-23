from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database  import get_db
from schemas.maintenance import MaintenanceResponse, MaintenanceCreate
from dependencies import get_current_user,RoleChecker
from models import UserRole
from crud import maintenance as crud_maintenance

router=APIRouter(prefix="/api/maintenance",tags=["维修记录"])
allow_edit = RoleChecker([UserRole.ADMIN, UserRole.EDITOR])

#维修记录的路由
#添加维修记录接口思路：调schemas里的维修记录创建函数给前端
#然后调crud里create_maintenance函数来核实前端传进来的参数
@router.post("/",response_model=MaintenanceResponse)
async def add_maintenance(
        data:MaintenanceCreate,
        db:AsyncSession=Depends(get_db),
        current_user=Depends(allow_edit)
):
    return await crud_maintenance.create_maintenance(db, data.model_dump(),current_user.id)

#维修记录表路由
#思路：调用用户登录验证，然后连接db接口，然后调用crud维修记录表函数
@router.get("/")
async def list_maintenance(
        robot_id:int|None=None,
        db:AsyncSession=Depends(get_db),
        _user=Depends(get_current_user)
):
    return await crud_maintenance.get_maintenance_list(db,robot_id)

#统计维修费用和总周期路由接口
@router.get("/stats")
async def maintenance_cost(
        db:AsyncSession=Depends(get_db),
        _user=Depends(get_current_user)
):
    return await crud_maintenance.get_maintenance_cost_duration(db)




