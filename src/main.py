from doctest import debug
from fastapi import FastAPI
import uvicorn

from format_changer.router import router as format_changer_router
from auth.router import router as auth_router


app = FastAPI(
    title='convert_image_app'
)


app.include_router(format_changer_router)
app.include_router(auth_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host='localhost', port=8000, reload=True)
