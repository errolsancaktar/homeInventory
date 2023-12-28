from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from dotenv import dotenv_values
from pymongo import MongoClient
from api import router as asset_router
import api
import uvicorn
import logging

### Set up Logging ###

logger = logging.getLogger('Inventory')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
# fh = logging.FileHandler('spam.log')
# fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
# logger.addHandler(fh)
logger.addHandler(ch)

### Import Config ###
config = dotenv_values(".env")

### Set up Mongo ###
dbUri = f"mongodb://{config['DB_USER']}:{config['DB_PASS']}@{config['DB_SERVER']}/{config['DB_NAME']}?retryWrites=true&w=majority&authSource={config['DB_NAME']}"
print(dbUri)
invName = config["INSTANCE_NAME"]

### Perform Startup Functions ###


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        app.mongodb_client = MongoClient(dbUri)
        app.database = app.mongodb_client[config["DB_NAME"]]
        logger.info(f"Connected to {app.mongodb_client.get_database().name}!")
        yield
    except:
        logger.error("Unable to Connect to Mongo Database")

    # Shutdown
    app.mongodb_client.close()


### Define Fastapi Object ###
app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")

### Routes ###

app.include_router(asset_router, tags=["assets"], prefix="/api")


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "instance_name": invName})


@app.get("/items")
async def list_records(request: Request):
    assets = api.list_assets(request)
    # for i in assets:
    #     print(i)
    return templates.TemplateResponse("items.html", {"request": request, "assets": assets})


@app.get("/search/{field}/{value}")
async def list_records(value: str, field: str, request: Request):
    assets = api.search_assets(request=request, field=field, value=value)
    # for i in assets:
    #     print(i)
    return templates.TemplateResponse("items.html", {"request": request, "assets": assets})


# @app.get("/item/{id}")
# async def get_record(request: Request, id: str):
#     asset = api.find_asset(request=request, id=id)
#     logger.debug(asset)
#     return templates.TemplateResponse("item.html", {"request": request, "asset": asset})


@app.get("/edit/{id}")
async def update_record(request: Request, id: str):
    asset = api.find_asset(request=request, id=id)
    logger.debug(asset)
    return templates.TemplateResponse("edit.html", {"request": request, "asset": asset})


### Upstart ###
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0", port=8080, reload="true")
