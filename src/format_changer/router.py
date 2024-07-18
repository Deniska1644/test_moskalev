from fastapi import APIRouter, Depends, File, UploadFile, Form
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import FileResponse, StreamingResponse
from typing import Annotated
from enum import Enum

from format_changer.utils.pillow_cls import Pillow_image_transform
from auth.depends import get_current_user
from auth.shemas import User
from format_changer.shemas import Pillow_Resize_Shem



router = APIRouter(
    prefix='/convert',
    tags=['convert']
)

class ModelName(str, Enum):
    JPEG = "jpeg"
    PNG = "png"
    GIF = "gif"
    BMP = 'bmp'


@router.post('/resize/{wd}/{hg}')
async def get_file_resize(
    wd:int,
    hg:int,
    model_name:ModelName,
    file: UploadFile,     
    current_user: Annotated[User, Depends(get_current_user)]
    ):
    result = await Pillow_image_transform.resize_img(file,wd,hg, model_name)
    return FileResponse(path=f'images/{result}', filename=result, media_type='multipart/form-data')


@router.post('/compression/{per}')
async def get_file_compression(
    per:float,
    file: UploadFile, 
    model_name:ModelName,
    current_user: Annotated[User, Depends(get_current_user)]
    ):
    result = await Pillow_image_transform.compression(file,per,model_name)
    return FileResponse(path=f'images/{result}', filename=file.filename, media_type='multipart/form-data')


@router.post('/file/{x}/{y}')
async def watermark_photos(
    file: UploadFile, 
    watermark_file: UploadFile, 
    model_name:ModelName,
    x:int,
    y:int,
    current_user: Annotated[User, Depends(get_current_user)]
    ):
    result = await Pillow_image_transform.watermark_photo(file,watermark_file,(x,y),model_name)
    return 'ok'