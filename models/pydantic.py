from pydantic import BaseModel
from typing import Union, Optional


###### Application Related #######


class APIKeyRequest(BaseModel):
    username: str
    password: str


class GenericAPIRepsonse(BaseModel):
    status_code: int
    message: Optional[str] = None
    data: Union[dict, str, None] = None


class CatalogRequest(BaseModel):
    page_size: Optional[int] = 10


###### Magento API Related #######


# for paginated search results
class SearchCriteria(BaseModel):
    filter_groups: list
    page_size: int
    current_page: int


# Magento search response with some searchCriteria (like products, etc. follow this request body)
class SearchResponse(BaseModel):
    items: list
    search_criteria: SearchCriteria
    total_count: int
