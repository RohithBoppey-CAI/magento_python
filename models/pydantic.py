from pydantic import BaseModel
from typing import Union, Optional

class APIKeyRequest(BaseModel):
    username: str
    password: str

class GenericAPIRepsonse(BaseModel):
    status_code: int
    message: Optional[str] = None
    data: Union[dict, str, None] = None
    
class CatalogRequest(BaseModel):
    page_size: Optional[int] = 10