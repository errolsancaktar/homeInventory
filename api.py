from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List
import io
import qrcode
import logging as log
from starlette.responses import StreamingResponse
from models import Asset, AssetUpdate
import image


databaseName = "testdb"
try:
    router = APIRouter()
except:
    print("problem with api")


@router.post("/", response_description="Create a new asset", status_code=status.HTTP_201_CREATED, response_model=Asset)
def create_asset(request: Request, asset: Asset = Body(...)):
    asset = jsonable_encoder(asset)
    new_asset = request.app.database[databaseName].insert_one(asset)
    created_asset = request.app.database[databaseName].find_one(
        {"_id": new_asset.inserted_id}
    )

    return created_asset


@router.get("/", response_description="List all assets", response_model=List[Asset])
def list_assets(request: Request):
    assets = list(request.app.database[databaseName].find(limit=100))
    return assets


@router.get("/{id}", response_description="Get a single asset by id", response_model=Asset)
def find_asset(id: str, request: Request):
    if (asset := request.app.database[databaseName].find_one({"_id": id})) is not None:
        return asset
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Asset with ID {id} not found")


@router.put("/{id}", response_description="Update an asset", response_model=Asset)
def update_asset(id: str, request: Request, asset: AssetUpdate = Body(...)):
    asset = {k: v for k, v in asset.model_dump().items() if v is not None}
    if len(asset) >= 1:
        update_result = request.app.database[databaseName].update_one(
            {"_id": id}, {"$set": asset}
        )

        if update_result.modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail=f"Asset with ID: {id} not found")

    if (
        existing_asset := request.app.database[databaseName].find_one({"_id": id})
    ) is not None:
        return existing_asset

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Asset with ID: {id} not found")


@router.delete("/{id}", response_description="Delete an asset")
def delete_asset(id: str, request: Request, response: Response):
    delete_result = request.app.database[databaseName].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return response

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Asset with ID {id} not found")


@router.get("/qr/{assetId}", response_description="QR code for Asset {id}", response_model=Asset)
def qrcode_asset(assetId: str, request: Request):
    """
    Generates qr code for the asset id which should take you to the asset page of the item
    """

    log.debug(f"Generating QR for {assetId}")
    assetUrl = request.url_for("find_asset", id=assetId)
    log.debug(type(assetUrl))
    qr = qrcode.QRCode(
        box_size=12,
        border=5,
        version=None
    )
    qr.add_data(assetUrl)
    qr.make(fit=True)
    img = qr.make_image()
    buf = io.BytesIO()
    img.save(buf)
    buf.seek(0)
    qr_code = image.add_overlay_text(
        qr_in=buf, text=str(assetUrl))
    buf.seek(0)
    buffer = io.BytesIO()
    qr_code.save(buffer, format='PNG')
    buffer.seek(0)
    return StreamingResponse(buffer, media_type="image/png")
