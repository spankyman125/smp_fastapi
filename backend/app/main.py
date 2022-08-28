import pathlib
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routing.router import api_router
from fastapi_responses import custom_openapi

APP_PATH = pathlib.Path(__file__).parent.resolve()

app = FastAPI(
    title="SMP_API",
    description="An API for SMP application",
    version="0.2.0",
    docs_url='/api/docs',
    redoc_url='/api/redoc',
    openapi_url='/api/openapi.json'
)
# app.openapi = custom_openapi(app)
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

app.include_router(api_router)
