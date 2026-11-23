from pydantic import BaseModel
from datetime import datetime

#专门用于接收机器人上传的数据。
class ParamUpload(BaseModel):
    name:str
    value:float
    unit:str
    min_threshold:float
    max_threshold:float

#返回给前端的参数回应
class ParamResponse(ParamUpload):
    id:int
    robot_id:int
    is_abnormal:bool
    created_at:datetime

    model_config = {'from_attributes':True}

