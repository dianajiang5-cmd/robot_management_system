from pydantic import BaseModel
from typing import Dict,List

#告诉前端需要返回什么格式的数据
class DashboardOverview(BaseModel):
    total_robots:int
    online_robots:int
    online_rate:str
    active_alerts:int
    abnormal_params_rate:str
    status_distribution:Dict[str,int]
    