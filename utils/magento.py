from models import APIKeyRequest, GenericAPIRepsonse, CatalogRequest
from .magento_links import MAGENTO_LINKS
import requests
from .validators import validate_response


@validate_response
def generate_magento_api_key(request: APIKeyRequest) -> GenericAPIRepsonse:
    try:
        link = MAGENTO_LINKS.get("GENERATE_API_KEY", None)
        if not link:
            return GenericAPIRepsonse(
                status_code=500,
                message="Magento API key generation URL is not configured",
                data=None,
            )
        request_body = {
            "username": request.username,
            "password": request.password,
        }
        result = requests.post(url=link, json=request_body, verify=False)

        status_code = result.status_code
        result = result.json()

        # logic to validate the user
        if isinstance(result, dict) and result.get("message") is not None:
            return GenericAPIRepsonse(status_code=500, message=result["message"])

        return GenericAPIRepsonse(status_code=status_code, data=result)
    except Exception as e:
        return GenericAPIRepsonse(
            status_code=500, message=f"Unexpected error: {str(e)}", data=None
        )


@validate_response
def retrive_store_products(request: CatalogRequest, token: str) -> GenericAPIRepsonse:
    try:
        retrive_store_products_link = MAGENTO_LINKS.get("RETRIVE_PRODUCTS", None)
        if not retrive_store_products_link:
            return GenericAPIRepsonse(
                status_code=500,
                message="Magento products retriveal URL is not configured",
                data=None,
            )

        params = {"searchCriteria[pageSize]": request.page_size}
        headers = {"Authorization": f"Bearer {token}"}

        result = requests.get(
            url=retrive_store_products_link,
            headers=headers,
            verify=False,
            params=params,
        )

        status_code = result.status_code
        
        return GenericAPIRepsonse(status_code=status_code, data=result.json())

    except Exception as e:
        return GenericAPIRepsonse(
            status_code=500, message=f"Unexpected error: {str(e)}", data=None
        )
