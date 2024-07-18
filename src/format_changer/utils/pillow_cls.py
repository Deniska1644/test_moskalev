from msilib import Binary
from re import split
from PIL import Image, ImageDraw
from fastapi import UploadFile



class Pillow_image_transform:

    @classmethod
    async def save(cls, result, name:str, format:str, file_format:str) -> str:
        if file_format != 'png':
            result.save (f'images/{name}.{format}', format = format)
            # print(result.)
            return f'{name}.{format}'
        else:
            result.convert('RGB')
            result.save(f'images/{name}.{format}', format = format)
            return f'{name}.{format}'

    
    @classmethod
    async def resize_img(cls, file, width:int,length:int, format:str) -> str:
        image = Image.open(file.file)
        result = image.resize((width, length))
        file_name, file_format = file.filename.split('.')
        full_name = await cls.save(result, file_name, format, file_format)
        return full_name
 

    @classmethod
    async def compression(cls,file, per:float, format:str) -> str:
        image = Image.open(file.file)
        width, height = image.size
        result = image.resize((int(width * per), int(height *per))) 
        file_name, file_format = file.filename.split('.')
        full_name = await cls.save(result, file_name, format, file_format)
        return full_name
      
    
    @classmethod
    async def watermark_photo(cls, file, watermark_file, position:tuple, format:str):
        image = Image.open(file.file)
        watermark = Image.open(watermark_file.file)
        width, height = image.size

        # result = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        # result.paste(image, (0, 0))
        # result.paste(watermark, position, mask=watermark)
        watermark = watermark.convert("RGBA")
        watermark_mask = watermark.split()[3]
        image.paste(watermark, position, mask=watermark_mask)
        
        file_name, file_format = file.filename.split('.')
        full_name = await cls.save(image, file_name, format, file_format)
        return full_name

        # if watermark.width >= self.wd or watermark.height >= self.hg:
        #     result = self.img.paste(watermark, position)
        #     return result
        # return 'ошибка размеров'

        