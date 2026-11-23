

from fastapi import FastAPI,Request
from contextlib import asynccontextmanager
import traceback

from starlette.responses import JSONResponse

from database import create_db_tables
from routers import user,robot,site,monitor,alert,maintenance,dashboard
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(_app:FastAPI):
    #启动程序时自动建表
    print('正在初始化数据库')
    await create_db_tables()
    print('数据库模型类更新完毕!')
    yield

app=FastAPI(
    title='Robot FastAPI',
    lifespan=lifespan
)
#中间键cors解决跨域前后端不同源的问题，协议，域名，端口这三个一致才是同源
app.add_middleware (
        CORSMiddleware,# type: ignore
        allow_origins=["*"],# type: ignore #允许的源开发阶段运行所有源，生产环境需要指定源
        allow_credentials=False,# type: ignore #携带cookie
        allow_methods=["*"],# type: ignore #允许请求方法
        allow_headers=["*"],# type: ignore #允许请求头
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    print(f"========== 捕获全局异常: {request.url} ==========")
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error", "error": str(exc)},
    )

@app.get('/')
def root():
    return{'message':'Hello world'}

#注册路由/挂载路由
app.include_router(user.router)
app.include_router(robot.router)
app.include_router(site.router)
app.include_router(monitor.router)
app.include_router(alert.router)
app.include_router(maintenance.router)
app.include_router(dashboard.router)

if __name__ == "__main__":
    # 启动 uvicorn 服务器
    uvicorn.run(
        "main:app",          # 模块名:实例名
        host="127.0.0.1",    # 主机地址
        port=8000,           # 端口号
        reload=True          # 开启热重载（修改代码自动重启）
    )
