from models import APIKeyRequest, GenericAPIRepsonse, CatalogRequest, SearchResponse
from .magento_links import MAGENTO_LINKS
import time
import requests
from .validators import validate_response
from .file import save_as_file_local


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
def retrive_store_products(
    request: CatalogRequest, token: str, bulk=False, save=False
) -> GenericAPIRepsonse:
    try:
        retrive_store_products_link = MAGENTO_LINKS.get("RETRIVE_PRODUCTS", None)
        if not retrive_store_products_link:
            return GenericAPIRepsonse(
                status_code=500,
                message="Magento products retriveal URL is not configured",
                data=None,
            )

        headers = {"Authorization": f"Bearer {token}"}
        page_number = 0
        offset = 0  # starting index for the product catalogue
        page_size = request.page_size

        STOPPING_CONDITION = 1 if bulk else (page_number != 1)
        response = {}

        while STOPPING_CONDITION:
            params = {
                "searchCriteria[pageSize]": page_size,
                "searchCriteria[currentPage]": page_number,
            }

            response = requests.get(
                retrive_store_products_link,
                headers=headers,
                params=params,
                verify=False,
            )

            if response.status_code != 200:
                return GenericAPIRepsonse(
                    status_code=500,
                    message=f"Error retrieving page {page_number}: {response.text}",
                    data=None,
                )

            # to validate the response
            valid_response = SearchResponse(**response.json())

            # response is successful, put it in a json file in the folder
            page_number += 1
            offset = page_number * page_size  # new offset
            STOPPING_CONDITION = (
                (offset <= valid_response.total_count) if bulk else (page_number != 1)
            )

            if save:
                save_as_file_local(
                    base_dir="./products",
                    file_name=f"products_{page_number}.json",
                    data=response.json(),
                )
                if bulk:
                    time.sleep(10)

        return (
            GenericAPIRepsonse(status_code=200, data=response.json())
            if not bulk
            else GenericAPIRepsonse(
                status_code=200, data={"status": "Bulk operation completed"}
            )
        )

    except Exception as e:
        return GenericAPIRepsonse(
            status_code=500, message=f"Unexpected error: {str(e)}", data=None
        )
