from pydantic import BaseModel, Field
from datetime import datetime

#告警的标记 前端传入和响应
class AlertResolve(BaseModel):
    resolve_note:str=Field(...,description='处理备注')

class AlertResponse(BaseModel):
    id:int
    robot_id:int
    message:str
    level:str
    is_resolved:bool
    resolver_id:int|None
    resolve_note:str|None
    resolved_date:datetime|None
    created_at:datetime

    model_config = {'from_attributes':True}

    