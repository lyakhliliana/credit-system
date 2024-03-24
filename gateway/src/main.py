import httpx
from fastapi import FastAPI, HTTPException

from gateway.src.models.dto import ProductDto, ApplicationCreateDto

app = FastAPI(
    title='Gateway API',
    summary='Documentation of Fintech Credits API - gateway',
    description='There will be some description of Fintech API',
    version='1.0.0'
)

host = 'http://172.29.176.1'


@app.get(
    '/product',
    summary='Get list of available products'
)
async def get_all_products():
    """
    Retrieve all products.
    :return: List of Json represented products
    """
    url = f"{host}:30/product"
    async with httpx.AsyncClient() as client:
        response = (await client.get(url))
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())


@app.get(
    '/product/{code}',
    response_model=ProductDto,
    summary='Get the specified product'
)
async def get_product(code: str) -> ProductDto:
    """

    :param code: Code of product to retrieve
    :return: if product code is available, then retrieve product info, else Not Found
    """
    url = f"{host}:30/product/{code}"
    async with httpx.AsyncClient() as client:
        response = (await client.get(url))
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())


@app.post('/application', summary='Clients request to create agreement')
async def application_request_create(application_to_post: ApplicationCreateDto):
    """
    Create new agreement of person.
    :param application_to_post: agreement data
    :return: Agreement id, otherwise 400, 409
    """
    url = f"{host}:30/application"
    async with httpx.AsyncClient() as client:
        response = (await client.post(url, json=application_to_post.model_dump()))
        if response.is_success:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())


@app.post('/application/{agreement_id}/close', summary='Clients request to cancel agreement')
async def application_request_cancel(agreement_id: int):
    """
        Close the agreement of person.
        :param agreement_id: agreement data
        :return: Agreement id, otherwise 400, 409
    """
    url = f"{host}:30/application/{agreement_id}/close"
    async with httpx.AsyncClient() as client:
        response = (await client.post(url, json=dict(agreement_id=agreement_id, )))
        if response.is_success:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())
