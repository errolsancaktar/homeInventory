from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import dotenv_values
from pymongo import MongoClient
import logging as log
from api import router as asset_router

### Set up Loggin ###
log.basicConfig(level=log.DEBUG)

### Import Config ###
config = dotenv_values(".env")

### Set up Mongo ###
dbUri = f"mongodb://{config['DB_USER']}:{config['DB_PASS']}@{config['DB_SERVER']}/{config['DB_NAME']}?retryWrites=true&w=majority&authSource={config['DB_NAME']}"
invName = config["INSTANCE_NAME"]

### Perform Startup Functions ###


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        app.mongodb_client = MongoClient(dbUri)
        app.database = app.mongodb_client[config["DB_NAME"]]
        log.info(f"Connected to {app.mongodb_client.get_database().name}!")
        yield
    except:
        log.error("Unable to Connect to Mongo Database")

    # Shutdown
    app.mongodb_client.close()


### Define Fastapi Object ###
app = FastAPI(lifespan=lifespan)


### Routes ###

app.include_router(asset_router, tags=["assets"], prefix="/api")


@app.get("/")
async def root():
    return {"message": f"Welcome to {invName} Inventory"}
