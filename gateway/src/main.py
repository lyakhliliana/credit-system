from fastapi import FastAPI

from gateway.src.endpoints.application import application_router
from gateway.src.endpoints.product import product_router

app = FastAPI(
    title='Gateway API',
    summary='Documentation of Fintech Credits API - gateway',
    description='There will be some description of Fintech API',
    version='1.0.0'
)

app.include_router(application_router)
app.include_router(product_router)
