import pathlib
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routing.router import api_router
from fastapi_responses import custom_openapi

APP_PATH=pathlib.Path(__file__).parent.resolve()

app = FastAPI()
app.openapi = custom_openapi(app)
es_client = AsyncElasticsearch("http://elastic:9200")

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("shutdown")
async def app_shutdown():
    await es_client.close()

app.mount("/static/images", StaticFiles(directory="app/static/images"), name="static_images")
app.mount("/static/css", StaticFiles(directory="app/static/css"), name="static_css")
app.mount("/static/js", StaticFiles(directory="app/static/js"), name="static_js")
app.include_router(api_router)

