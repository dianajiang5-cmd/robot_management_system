from fastapi import APIRouter, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from schemas.site import SiteCreate,SiteResponse
from crud import site as crud_site
from dependencies import get_current_user,RoleChecker
from models import UserRole
from typing import List
from fastapi import Depends


router=APIRouter(prefix="/api/site",tags=["站点管理"])
#定义权限：只有admin和editor能增删除改
allow_edit=RoleChecker([UserRole.ADMIN,UserRole.EDITOR])

#增加站点
@router.post("/",response_model=SiteResponse)
async def add_site(
    site_in:SiteCreate,
    db: AsyncSession = Depends(get_db),
    _current_user=Depends(get_current_user)
):
    #先查重
    existing_site=await crud_site.get_site_by_name(db,site_in.site_name)
    if existing_site:
        raise HTTPException(status_code=400,detail="该站点名称已存在")
    return await crud_site.create_site(db,site_in.model_dump())

#获取站点列表所有用户都可以查看
@router.get("/",response_model=List[SiteResponse])
async def get_site_list(
    db: AsyncSession = Depends(get_db),
    _current_user=Depends(get_current_user)
):
    return await crud_site.get_sites(db)

#获取单个站点详情信息
@router.get("/{site_id}",response_model=SiteResponse)
async def get_site_detail(
    site_id:int,
    db: AsyncSession = Depends(get_db),
    _current_user=Depends(get_current_user)
):
    site=await crud_site.get_site_by_id(db,site_id)
    if not site:
        raise HTTPException(status_code=404,detail="该站点不存在")
    return site

#更新站点信息
@router.put("/{site_id}",response_model=SiteResponse)
async def update_site(
    site_id: int,
    site_in:SiteCreate,
    db: AsyncSession = Depends(get_db),
    _current_user=Depends(allow_edit)
):
    site=await crud_site.get_site_by_id(db,site_id)
    if not site:
        raise HTTPException(status_code=404,detail='该站点不存在')
    return await crud_site.update_site(db,site,site_in.model_dump())

#删除站点
@router.delete("/{site_id}")
async  def delete_site(
    site_id:int,
    db: AsyncSession = Depends(get_db),
    _current_user=Depends(allow_edit)
):
    site=await crud_site.delete_site(db,site_id)# type: ignore
    if not site:
        raise HTTPException(status_code=404,detail="该站点不存在")
    await crud_site.delete_site(db,site_id)# type: ignore
    return{'message':'该站点删除成功'}
