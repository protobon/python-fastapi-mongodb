from datetime import datetime
from app.schema.base import CustomBaseModel, Body, Response
from pydantic import Field
from typing import List, Optional


class ProductSchema(CustomBaseModel):
    id: str = Field(None, description="Unique document id")
    title: str = Field(None, description="Product title", min_length=2, max_length=125)
    quantity: int = Field(0, description="Quantity (units)", ge=0)
    createdAt: datetime = Field(None, description="Creation date")


class FetchProductSchema(CustomBaseModel):
    products: List[ProductSchema] = []
    total: int = 0


class FetchProductBody(Body):
    data: Optional[FetchProductSchema] = None


class FetchProductResponse(Response):
    body: FetchProductBody


class NewProductSchema(CustomBaseModel):
    title: str = Field(None, description="Product title", min_length=2, max_length=125)
    quantity: int = Field(0, description="Quantity (units)", ge=0)
    createdAt: datetime = Field(None, description="Creation date")


class NewProductBody(Body):
    data: Optional[ProductSchema] = None


class NewProductResponse(Response):
    body: NewProductBody
