from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Alert


#告警的crud执行
#查告警列表按照状态过滤
async def get_alerts(db:AsyncSession,is_resolved:bool|None=None):
    stmt=select(Alert)
    if is_resolved is not None:
        stmt=stmt.where(Alert.is_resolved==is_resolved)
    stmt=stmt.order_by(Alert.created_at.desc())
    result=await db.execute(stmt)
    return result.scalars().all()

#标记已解决
async def resolve_alert(db:AsyncSession,alert_id:int,user_id:int,note:str):
    stmt=select(Alert).where(Alert.id==alert_id)
    result=await db.execute(stmt)
    alert=result.scalar_one_or_none()

    if alert:
        alert.is_resolved=True
        alert.resolver_id=user_id
        alert.resolve_note=note
        alert.resolved_date=datetime.now()

        await db.commit()
        await db.refresh(alert)
    return alert


