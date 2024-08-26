from fastapi import APIRouter

from app.products.core import ProductScrapping
from app.products.schemas import SearchQuery, SearchResponse

router = APIRouter()

@router.post("/search/", response_model=SearchResponse)
def search(data: SearchQuery):
    data = ProductScrapping().get_products(data=data)
    status, message = (True, "Success") if data else (False, "There are no results")

    return SearchResponse(status=status, message=message, data=data)
