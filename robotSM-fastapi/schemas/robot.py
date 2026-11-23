from pydantic import BaseModel,computed_field
from datetime import date, datetime

#schemas里面写的是创建站点新增时前端提交的数据
#Pydantic,校验前端传过来的参数信息

#创建机器人时前端需要按照以下信息传参
class RobotCreate(BaseModel):
    name:str
    robot_type:str
    site_id:int
    purchase_date:date
    warranty_end_date:date

class RobotUpdate(BaseModel):
    name: str | None = None
    status: str | None = None
    robot_type: str | None = None
    ip_address: str | None = None
    site_id: int | None = None

#前端传参进来后返回前端的参数信息
class RobotResponse(BaseModel):
    id:int
    ip_address:str|None
    name:str
    status:str
    robot_type:str
    site_id:int
    created_by:str|None
    created_at:datetime
    purchase_date:date
    warranty_end_date:date

    model_config = {"from_attributes": True}  # 允许从 ORM 模型读取数据
#动态计算使用时长
    @computed_field
    @property
    def usage_days(self)->int:
        return (date.today() - self.purchase_date).days

#计算保修状态
    @computed_field
    @property
    def warranty_status(self)->str:

        if date.today()>self.warranty_end_date:
            return '已过保'
        else:
            return '保修中'
    model_config={'from_attributes':True}

