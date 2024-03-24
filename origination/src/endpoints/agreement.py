from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from common.generic_repository import GenericRepository
from common.scoring_status import Status
from origination.src.models.dao import AgreementDao
from origination.src.models.dto import AgreementDto, AgreementCreateDto
from origination.src.models.session_maker import get_session

agreement_router = APIRouter(prefix='/agreement')


@agreement_router.get(
    '/{agreement_id}',
    response_model=AgreementDto,
    summary='Get the specified agreement'
)
async def get_agreement_by_id(agreement_id: int, session: AsyncSession = Depends(get_session)) -> AgreementDto:
    """
    :param agreement_id: id of agreement to retrieve
    :param session: The connection session with DB
    :return: if agreement id is available, then retrieve product info, else Not Found
    """
    repository = GenericRepository(session, AgreementDao)
    agreement_dao: AgreementDao = (await repository.get_one_by_params(['agreement_id'], [agreement_id]))
    if agreement_dao is None:
        raise HTTPException(status_code=404, detail='Not found')
    return AgreementDto(agreement_id=agreement_dao.agreement_id, status=agreement_dao.status)


@agreement_router.post('',
                       response_model=AgreementDto,
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
    agreement: AgreementDao = (await repository.get_one_by_params(
        ['agreement_id'],
        [agreement_to_post.agreement_id]
    ))
    if agreement:
        return agreement.convert_to_dto()

    agreement_n = AgreementDao(agreement_id=agreement_to_post.agreement_id, status=Status.NEW.value)
    await repository.save(agreement_n)
    return agreement_n.convert_to_dto()


@agreement_router.get(
    '/new',
    response_model=list[AgreementDto],
    summary='Get list of new agreements'
)
async def get_new_agreements(session: AsyncSession = Depends(get_session)) -> list[AgreementDto]:
    """
    Retrieve all new agreements.
    :param session: The connection session with DB
    :return: List of Json represented agreements with status NEW
    """
    agreements: Sequence[AgreementDao] = (await GenericRepository(session, AgreementDao).get_all_by_params_and(
        ['status', ],
        [Status.NEW.value, ]
    ))
    if len(agreements) == 0:
        raise HTTPException(status_code=404, detail='Not found')
    return [agreement.convert_to_dto() for agreement in agreements]


@agreement_router.get(
    '/scored',
    response_model=list[AgreementDto],
    summary='Get list of scored agreements'
)
async def get_scored_agreements(session: AsyncSession = Depends(get_session)) -> list[AgreementDto]:
    """
    Retrieve all scored agreements.
    :param session: The connection session with DB
    :return: List of Json represented agreements with status REJECT and APPROVED
    """
    agreements: Sequence[AgreementDao] = (await GenericRepository(session, AgreementDao).get_all_by_params_or(
        ['status', 'status', ],
        [Status.REJECTED.value, Status.APPROVED.value, ]
    ))
    if len(agreements) == 0:
        raise HTTPException(status_code=404, detail='Not found')
    return [agreement.convert_to_dto() for agreement in agreements]
