from pydantic import BaseModel
from datetime import datetime

#schemas里面写的是创建站点新增时前端提交的数据
#Pydantic,校验前端传过来的参数信息

#增加站点接口
class SiteCreate(BaseModel):
    site_name:str
    location:str|None = None

#删除站点，更改站点信息，查看站点信息

#返回给前端的响应
class SiteResponse(SiteCreate):
    id:int
    is_active:bool
    created_at:datetime
    updated_at:datetime

    model_config = {'from_attributes':True}
