from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas.dashboard import DashboardOverview
from crud.dashboard import get_dashboard_stats
from dependencies import get_current_user
from cache.cache_config import get_json,set_cache


router=APIRouter(prefix="/api/dashboard",tags=["仪表盘统计"])

#每次查询数据库之前先去redis里面找有没有现成
@router.get("/",response_model=DashboardOverview)
async def get_overview(
        db:AsyncSession=Depends(get_db),
        _user=Depends(get_current_user)#只有登录才可以查看仪表盘信息
):
    cache_key="dashboard:overview"

    #1先尝试从redis里面获取数据
    cached_data=await get_json(cache_key)
    if cached_data:
        print("命中缓存，直接从redis返回数据")
        return cached_data
    #2缓存没有中或者过期，就去数据库里查
    print("缓存没有命中，执行复杂的sql查询")
    db_stats=await get_dashboard_stats(db)

    #3将查询结果写入redis设置300秒过期
    await set_cache(cache_key,db_stats,expire=3600)

    return db_stats

