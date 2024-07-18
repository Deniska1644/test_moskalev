from pydantic import BaseModel


class Pillow_Resize_Shem(BaseModel):
    wd : int
    legth: int



class Pillow_Comresiion_Shem(BaseModel):
    per: float


class Pillow(BaseModel):
    x: int
    y: int