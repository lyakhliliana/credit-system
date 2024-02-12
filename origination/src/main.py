from typing import Sequence
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database.generic_repository import GenericRepository
from database.http_output import JsonBeautify
from origination.src.models.dao import AgreementDao
from origination.src.models.dto import AgreementDto, AgreementCreateDto
from origination.src.models.session_maker import get_session

app = FastAPI(
    title='Origination API',
    summary='Documentation of Fintech Credits API - Origination',
    description='There will be some description of Fintech API',
    version='1.0.0',
)


@app.get(
    '/agreement/{id}',
    response_model=AgreementDto,
    response_class=JsonBeautify,
    summary='Get the specified agreement'
)
async def get_agreement_by_id(id: int | UUID, session: AsyncSession = Depends(get_session)) -> AgreementDto:
    """
    :param id: id of agreement to retrieve
    :param session: The connection session with DB
    :return: if agreement id is available, then retrieve product info, else Not Found
    """
    repository = GenericRepository(session, AgreementDao)
    product: AgreementDao = (await repository.get_one_by_params(['agreement_id'], [id]))
    if product is None:
        raise HTTPException(status_code=404, detail='Not found')
    return AgreementDto(id=product.id, status=product.status)


@app.get(
    '/new_agreements',
    response_model=list[AgreementDto],
    response_class=JsonBeautify,
    summary='Get list of new agreements'
)
async def get_new_agreements(session: AsyncSession = Depends(get_session)) -> list[AgreementDto]:
    """
    Retrieve all new agreements.
    :param session: The connection session with DB
    :return: List of Json represented agreements with status NEW
    """
    agreements: Sequence[AgreementDto] = (
        await GenericRepository(session, AgreementDto).get_all_by_params_and(["status", ], ["NEW", ]))
    return [AgreementDto(id=agreement.id, status=agreement.status) for agreement in agreements]


@app.get(
    '/scored_agreements',
    response_model=list[AgreementDto],
    response_class=JsonBeautify,
    summary='Get list of scored agreements'
)
async def get_scored_agreements(session: AsyncSession = Depends(get_session)) -> list[AgreementDto]:
    """
    Retrieve all scored agreements.
    :param session: The connection session with DB
    :return: List of Json represented agreements with status REJECT and APPROVED
    """
    agreements: Sequence[AgreementDto] = (
        await GenericRepository(session, AgreementDto).get_all_by_params_or(["status", "status", ],
                                                                            ["REJECT", "APPROVED", ]))
    return [AgreementDto(id=agreement.id, status=agreement.status) for agreement in agreements]


@app.post('/agreement',
          response_model=AgreementDto,
          response_class=JsonBeautify,
          summary='Add new agreement')
async def add_agreement(
        agreement_to_post: AgreementCreateDto,
        session: AsyncSession = Depends(get_session)
):
    """
    If agreement is not available, then create agreement in origination with status NEW.
    :param agreement_to_post: agreement to add
    :param session: The connection session with DB
    :return: If agreement not in DB, create, then return agreement
    """
    repository = GenericRepository(session, AgreementDao)
    agreement: AgreementDao = (await repository.get_one_by_params(['id'], [agreement_to_post.id]))
    if agreement:
        return agreement

    agreement_n = AgreementDto(id=agreement_to_post.id, status=agreement_to_post.status)
    await repository.save(agreement_n)
    return agreement_n

# import uvicorn
# if __name__ == "__main__":
#     uvicorn.run("main:app", port=80, log_level="info")
