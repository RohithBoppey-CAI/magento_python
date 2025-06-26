from fastapi import FastAPI
from routes import magento_router

app = FastAPI()

app.include_router(magento_router)
