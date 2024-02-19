from uuid import UUID

import httpx
import requests
from fastapi import FastAPI

from database.http_output import JsonBeautify
from gateway.src.models.dto import ProductDto, ApplicationCreateDto

app = FastAPI(
    title='Gateway API',
    summary='Documentation of Fintech Credits API - gateway',
    description='There will be some description of Fintech API',
    version='1.0.0'
)

host = "http://192.168.0.103"


@app.get(
    '/product',
    response_class=JsonBeautify,
    summary='Get list of available products'
)
async def get_all_products():
    """
    Retrieve all products.
    :return: List of Json represented products
    """
    url = f"{host}:30/product"
    return requests.get(url).json()


@app.get(
    '/product/{code}',
    response_model=ProductDto,
    response_class=JsonBeautify,
    summary='Get the specified product'
)
async def get_product(code: str) -> ProductDto:
    """

    :param code: Code of product to retrieve
    :return: if product code is available, then retrieve product info, else Not Found
    """
    url = f"{host}:30/product/{code}"
    return requests.get(url, params=dict(code=code, )).json()


@app.post('/application', summary='Clients request to create agreement')
async def application_request_create(
        application_to_post: ApplicationCreateDto
):
    """
    Create new agreement of person.
    :param application_to_post: agreement data
    :return: Agreement id, otherwise 400, 409
    """
    url = f"{host}:30/application"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=application_to_post.model_dump())
    return response.json()


@app.post('/application/{agreement_id}/close', summary='Clients request to cancel agreement')
async def application_request_cancel(
        agreement_id: int | UUID
):
    """
        Close the agreement of person.
        :param agreement_id: agreement data
        :return: Agreement id, otherwise 400, 409
    """
    url = f"{host}:30/application/{agreement_id}/close"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=dict(agreement_id=agreement_id,))
    return response.status_code
