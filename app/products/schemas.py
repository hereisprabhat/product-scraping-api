from typing import List, Optional

from pydantic import BaseModel, HttpUrl

from app.products.examples import ex_product


class Product(BaseModel):
    name: Optional[str] = ""
    price: Optional[str] = ""
    image_url: Optional[HttpUrl] = ""

    class Config:
        schema_extra = {"example": ex_product}


class SearchQuery(BaseModel):
    pages: Optional[int] = 0
    proxy: Optional[str] = ""


class SearchResponse(BaseModel):
    status: bool = True
    message: str = "Success"
    data: List[Product]
