from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models import Site

#通过站点名称查重
async def get_site_by_name(
        db: AsyncSession,
        site_name: str
):
    stmt=select(Site).where(Site.site_name==site_name)
    result=await db.execute(stmt)
    return result.scalar_one_or_none()

#通过站点ID来查详情信息
async def get_site_by_id(
        db: AsyncSession,
        site_id: int
):
    stmt=select(Site).where(Site.id==site_id)
    result=await db.execute(stmt)
    return result.scalar_one_or_none()

#新增站点
async def create_site(
        db: AsyncSession,
        site_date:dict
):
    new_site = Site(**site_date)
    db.add(new_site)
    await db.commit()
    await db.refresh(new_site)
    return new_site

#查站点列表接口
async def get_sites(db: AsyncSession):
    stmt=select(Site)
    result=await db.execute(stmt)
    return result.scalars().all()

#更新站点
async def update_site(
        db: AsyncSession,
        db_site: Site,
        update_data:dict
):
    for key,value in update_data.items():
        setattr(db_site,key,value)
    await db.commit()
    await db.refresh(db_site)
    return db_site

#删除站点
async  def delete_site(db: AsyncSession,db_site:Site):
    await db.delete(db_site)
    await db.commit()







