from fastapi import FastAPI
from contextlib import asynccontextmanager
from dotenv import dotenv_values
from pymongo import MongoClient
from api import router as asset_router
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


### Routes ###

app.include_router(asset_router, tags=["assets"], prefix="/api")


@app.get("/")
async def root():
    return {"message": f"Welcome to {invName} Inventory"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0", port=8080, reload="true", debug=True)
