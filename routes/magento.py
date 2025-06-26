from fastapi import APIRouter, Header, HTTPException
from models import APIKeyRequest, CatalogRequest
from utils import generate_magento_api_key, retrive_store_products

magento_router = APIRouter(prefix="/magento", tags=["Magento"])


def get_token(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token format")
    return authorization.split(" ")[1]


@magento_router.post("/generate_api_key")
def generate_api_key(request: APIKeyRequest):
    api_key = generate_magento_api_key(request)
    return api_key


@magento_router.post("/retrieve_products")
def retreive_products(request: CatalogRequest, token):
    return retrive_store_products(request, token)


@magento_router.post("/bulk/retrieve_products")
def retreive_products_bulk(request: CatalogRequest, token):
    return retrive_store_products(request, token, bulk=True, save=True)
