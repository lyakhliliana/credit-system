import os

import httpx
from fastapi import APIRouter, HTTPException

from gateway.src.models.dto import AgreementDto

agreement_router = APIRouter(prefix='/agreement')

host = os.getenv('PRODUCT_ENGINE_HOST')
port = os.getenv('PRODUCT_ENGINE_PORT')


@agreement_router.get(
    '/{person_id}',
    response_model=list[AgreementDto],
    summary='Get the agreements of person'
)
async def get_person_agreements(person_id: int) -> list[AgreementDto]:
    """
    :param person_id: id of person
    :return: list of agreements
    """
    url = f'{host}:{port}/agreements/{person_id}'
    async with httpx.AsyncClient() as client:
        response = (await client.get(url))
        if response.status_code == 200:
            return response.json()
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())

