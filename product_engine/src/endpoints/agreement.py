from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from common.generic_repository import GenericRepository
from product_engine.src.models.dao import AgreementDao
from product_engine.src.models.dto import AgreementDto
from product_engine.src.models.session_maker import get_session

agreement_router = APIRouter(prefix="/agreement")


@agreement_router.get(
    's/{person_id}',
    response_model=list[AgreementDto],
    summary='Get the agreements of person'
)
async def get_agreements_by_person(person_id: int, session: AsyncSession = Depends(get_session)) -> list[AgreementDto]:
    """
    :param person_id: id of person
    :param session: The connection session with DB
    :return: list of agreements
    """
    agreements: Sequence[AgreementDao] = (
        await GenericRepository(session, AgreementDao).get_all_by_condition(
            AgreementDao.person_id == person_id))
    return [agreement.convert_to_dto() for agreement in agreements]


@agreement_router.get(
    '/{agreement_id}',
    response_model=AgreementDto,
    summary='Get the agreement by id.'
)
async def get_agreement(agreement_id: int, session: AsyncSession = Depends(get_session)) -> AgreementDto:
    """
    :param agreement_id: id of agreement
    :param session: The connection session with DB
    :return: agreement
    """
    agreement: AgreementDao = (
        await GenericRepository(session, AgreementDao).get_one_by_condition(
            AgreementDao.agreement_id == agreement_id))
    return agreement.convert_to_dto()


@agreement_router.post('/{agreement_id}', summary='Update status by id')
async def change_agreement_status(agreement_id: int, status: str, session: AsyncSession = Depends(get_session)):
    repository = GenericRepository(session, AgreementDao)
    agreement: AgreementDao = (await repository.get_one_by_condition(AgreementDao.agreement_id == agreement_id))
    if agreement is None:
        raise HTTPException(status_code=404, detail='Заявки с указанным ID не существует.')

    await repository.update_property(
        ['agreement_id'],
        [agreement.agreement_id],
        'status',
        status
    )
