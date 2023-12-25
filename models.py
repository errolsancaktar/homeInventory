import uuid
from typing import Optional
from pydantic import BaseModel, Field, PastDate, PositiveFloat
from datetime import date, timedelta


class Asset(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    description: str = Field(None)
    site: str = Field(None, alias='main_location')
    location: str = Field(None, alias='specific_location')
    purchaseDate: PastDate = Field(None)
    manufacturer: str = Field(None)
    model: str = Field(None)
    serial: str = Field(None)
    originalCost: PositiveFloat = Field(None)
    estimatedValueA: PositiveFloat = Field(None)
    estimatedValueB: PositiveFloat = Field(None)
    owner: str = Field(None)
    assetImage: str = Field(None)
    receipt: str = Field(None)

    class Config:
        populate_by_name = True
        exclude_unset = True
        extra = "forbid"
        json_schema_extra = {
            "example": {
                "name": "Samsung 75 TV",
                "description": "smart tv",
                "site": "house",
                "location": "room",
                "purchaseDate": '2023-12-01',
                "manufacturer": "Samsung",
                "model": "sam75big",
                "serial": "1231214124",
                "originalCost": 12.23,
                "estimatedValueA": 12.50,
                "estimatedValueB": 100.00,
                "owner": "user1",
                "assetImage": "/mnt/stor",
                "receipt": "/mnt/recp",

            }
        }


class AssetUpdate(BaseModel):
    name: str = Field(None)
    description: str = Field(None)
    site: str = Field(None, alias='main_location')
    location: str = Field(None, alias='specific_location')
    purchaseDate: PastDate = Field(None)
    manufacturer: str = Field(None)
    model: str = Field(None)
    serial: str = Field(None)
    originalCost: PositiveFloat = Field(None)
    estimatedValueA: PositiveFloat = Field(None)
    estimatedValueB: PositiveFloat = Field(None)
    owner: str = Field(None)
    assetImage: str = Field(None)
    receipt: str = Field(None)

    class Config:
        populate_by_name = True
        exclude_unset = True
        extra = "forbid"
        json_schema_extra = {
            "example": {
                "name": "Samsung 75 TV",
                "description": "smart tv",
                "site": "house",
                "location": "room",
                "purchaseDate": '2023-12-01',
                "manufacturer": "Samsung",
                "model": "sam75big",
                "serial": "1231214124",
                "originalCost": 12.23,
                "estimatedValueA": 12.50,
                "estimatedValueB": 100.00,
                "owner": "user1",
                "assetImage": "/mnt/stor",
                "receipt": "/mnt/recp",

            }
        }
