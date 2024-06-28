import os

import httpx
from fastapi import APIRouter, HTTPException

from gateway.src.models.dto import PaymentDto

payment_router = APIRouter(prefix='/payment')

host = os.getenv('PRODUCT_ENGINE_HOST')
port = os.getenv('PRODUCT_ENGINE_PORT')


@payment_router.get(
    's/{agreement_id}',
    response_model=list[PaymentDto],
    summary='Get the schedule by agreement_id'
)
async def get_payments(agreement_id: int) -> list[PaymentDto]:
    """
    :param agreement_id: id of agreement
    :return: list of payments
    """
    url = f'{host}:{port}/payments/{agreement_id}'
    async with httpx.AsyncClient() as client:
        response = (await client.get(url))
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())