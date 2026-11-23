from fastapi import APIRouter, Depends, HTTPException
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from dependencies import get_current_user, RoleChecker
from models import UserRole
from schemas.alert import AlertResponse, AlertResolve
from crud import alert as crud_alert


router=APIRouter(prefix="/api/alert",tags=["告警"])
allow_edit = RoleChecker([UserRole.ADMIN, UserRole.EDITOR])

#告警列表查询
@router.get('/',response_model=List[AlertResponse])
async def list_alerts(
        is_resolved:bool|None=None,
        db:AsyncSession=Depends(get_db),
        _user=Depends(get_current_user)
):
    return await crud_alert.get_alerts(db,is_resolved)

#告警标记处理接口
@router.put("/{alert_id}/resolve")
async def mark_alert_resolve(
        alert_id:int,
        data:AlertResolve,
        db:AsyncSession=Depends(get_db),
        current_user=Depends(allow_edit)
):
    alert=await crud_alert.resolve_alert(db,alert_id,current_user.id,data.resolve_note)
    if not alert:
        raise HTTPException(status_code=404,detail='告警不存在')
    return {"msg":"告警已标记已解决","alert":alert}


