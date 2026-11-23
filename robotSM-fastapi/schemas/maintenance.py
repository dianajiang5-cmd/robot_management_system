from datetime import datetime
from pydantic import BaseModel


#维修记录
class MaintenanceCreate(BaseModel):
    robot_id:int
    maintain_type:str
    description:str
    cost:float=0.0
    duration:int =0


class MaintenanceResponse(BaseModel):
    id:int
    site_name:str
    performer_id:int
    created_at:datetime

    model_config = {"from_attributes":True}