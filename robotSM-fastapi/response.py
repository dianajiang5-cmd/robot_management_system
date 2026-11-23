from fastapi.responses import JSONResponse
from fastapi.encoders import  jsonable_encoder

#项目里任何成功响应都可以调这个函数
def success_response(message:str='success',data=None):
    content={
        'code':200,
        'message':message,
        'data':data
    }
    return JSONResponse(content=jsonable_encoder(content))
