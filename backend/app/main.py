from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routing.router import api_router
import pathlib
APP_PATH=pathlib.Path(__file__).parent.resolve()

app = FastAPI()
app.mount("/static/images", StaticFiles(directory="app/static/images"), name="static_images")
app.mount("/static/css", StaticFiles(directory="app/static/css"), name="static_css")
app.mount("/static/js", StaticFiles(directory="app/static/js"), name="static_js")
app.include_router(api_router)