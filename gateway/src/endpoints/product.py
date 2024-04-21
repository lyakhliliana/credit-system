import os

import httpx
from fastapi import APIRouter, HTTPException

from gateway.src.models.dto import ProductDto

product_router = APIRouter(prefix='/product')

host = os.getenv('PRODUCT_ENGINE_HOST')
port = os.getenv('PRODUCT_ENGINE_PORT')


@product_router.get(
    '',
    summary='Get list of available products'
)
async def get_all_products():
    """
    Retrieve all products.
    :return: List of Json represented products
    """
    url = f'{host}:{port}/product'
    async with httpx.AsyncClient() as client:
        response = (await client.get(url))
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())


@product_router.get(
    '/{code}',
    response_model=ProductDto,
    summary='Get the specified product'
)
async def get_product(code: str) -> ProductDto:
    """

    :param code: Code of product to retrieve
    :return: if product code is available, then retrieve product info, else Not Found
    """
    url = f'{host}:{port}/product/{code}'
    async with httpx.AsyncClient() as client:
        response = (await client.get(url))
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())
