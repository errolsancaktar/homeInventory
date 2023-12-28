import uuid
from typing import Optional
from pydantic import BaseModel, Field, PastDate, PositiveFloat, field_validator
from typing import Union
from datetime import datetime

typeValues = ["Electronics", "Furniture"]


class Asset(BaseModel):
    id: Union[str, uuid.uuid4] = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    description: Optional[str] = None
    main_location: Optional[str] = None
    specific_location: Optional[str] = None
    purchaseDate: Optional[PastDate] = None
    manufacturer: Optional[str] = None
    model: Optional[str] = None
    serial: Optional[str] = None
    originalCost: Optional[PositiveFloat] = Field(None)
    estimatedValueA: Optional[PositiveFloat] = Field(None)
    estimatedValueB: Optional[PositiveFloat] = Field(None)
    owner: Optional[str] = None
    assetImage: Optional[str] = None
    receipt: Optional[str] = None
    type: Optional[str] = None
    group: Optional[str] = None
    roles: Optional[str] = None
    qty: int = Field(default=1)
    condition: Optional[str] = None
    highval: Union[None, Optional[bool]] = Field(default=False)
    warranty: Optional[str] = None
    modified: Optional[datetime] = None
    created: Optional[datetime] = None
    # @field_validator("type")
    # def validate_type(cls, v):
    #     assert v in typeValues
    #     return v

    class Config:
        populate_by_name = True
        exclude_unset = True
        extra = "ignore"
        json_schema_extra = {
            "example": {
                "name": "Samsung 75 TV",
                "description": "smart tv",
                "main_location": "house",
                "specific_location": "room",
                "purchaseDate": '2023-12-01',
                "manufacturer": "Samsung",
                "model": "sam75big",
                "serial": "1231214124",
                "roles": "users",
                "warranty": "1 Year",
                "qty": 1,
                "highval": False
            }

        }


class AssetUpdate(Asset):
    id: str = None
    name: Optional[str] = None

# class AssetUpdate(BaseModel):
#     name: str = Field(None)
#     description: str = Field(None)
#     main_location: str = Field(None, alias='main_location')
#     specific_location: str = Field(None, alias='specific_location')
#     purchaseDate: PastDate = Field(None)
#     manufacturer: str = Field(None)
#     model: str = Field(None)
#     serial: str = Field(None)
#     originalCost: PositiveFloat = Field(None)
#     estimatedValueA: PositiveFloat = Field(None)
#     estimatedValueB: PositiveFloat = Field(None)
#     owner: str = Field(None)
#     assetImage: str = Field(None)
#     receipt: str = Field(None)

#     class Config:
#         populate_by_name = True
#         exclude_unset = True
#         extra = "ignore"
#         json_schema_extra = {
#             "example": {
#                 "name": "Samsung 75 TV",
#                 "description": "smart tv",
#                 "main_location": "house",
#                 "specific_location": "room",
#                 "purchaseDate": '2023-12-01',
#                 "manufacturer": "Samsung",
#                 "model": "sam75big",
#                 "serial": "1231214124",
#                 "originalCost": 12.23,
#                 "estimatedValueA": 12.50,
#                 "estimatedValueB": 100.00,
#                 "owner": "user1",
#                 "assetImage": "/mnt/stor",
#                 "receipt": "/mnt/recp",

#             }
#         }
