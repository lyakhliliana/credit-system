import os

import httpx
from fastapi import APIRouter, HTTPException

from gateway.src.models.dto import ApplicationCreateDto

application_router = APIRouter(prefix='/application')

host = os.getenv('PRODUCT_ENGINE_PORT')
port = os.getenv('PRODUCT_ENGINE_PORT')


@application_router.post('', summary='Clients request to create agreement')
async def application_request_create(application_to_post: ApplicationCreateDto):
    """
    Create new agreement of person.
    :param application_to_post: agreement data
    :return: Agreement id, otherwise 400, 409
    """
    url = f'{host}:{port}/application'
    async with httpx.AsyncClient() as client:
        response = (await client.post(url, json=application_to_post.model_dump()))
        if response.is_success:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())


@application_router.post('/{agreement_id}/close', summary='Clients request to cancel agreement')
async def application_request_cancel(agreement_id: int):
    """
        Close the agreement of person.
        :param agreement_id: agreement data
        :return: Agreement id, otherwise 400, 409
    """
    url = f'{host}:{port}/application/{agreement_id}/close'
    async with httpx.AsyncClient() as client:
        response = (await client.post(url, json=dict(agreement_id=agreement_id, )))
        if response.is_success:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())
