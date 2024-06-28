from fastapi import APIRouter, Depends, HTTPException
from fastapi.openapi.models import Response
from sqlalchemy.ext.asyncio import AsyncSession

from common.generic_repository import GenericRepository
from origination.src.models.dao import AgreementDao
from origination.src.models.dto import AgreementDto, AgreementCreateDto
from origination.src.models.session_maker import get_session
from origination.src.utils.change_agreement_status import change_agreement_status
from origination.src.utils.create_agreement_db import create_agreement_db

agreement_router = APIRouter(prefix='/agreement')


@agreement_router.get(
    '/{agreement_id}',
    response_model=AgreementDto,
    summary='Get the specified agreement by id.'
)
async def get_agreement(agreement_id: int, session: AsyncSession = Depends(get_session)) -> AgreementDto:
    """
    :param agreement_id: id of agreement to retrieve
    :param session: The connection session with DB
    :return: if agreement id is available, then retrieve product info, else Not Found
    """
    repository = GenericRepository(session, AgreementDao)
    agreement: AgreementDao = (await repository.get_one_by_condition(AgreementDao.agreement_id == agreement_id))
    if agreement is None:
        raise HTTPException(status_code=404, detail='Not found.')
    return agreement.convert_to_dto()


@agreement_router.post('',
                       response_model=AgreementDto,
                       summary='Add new agreement.')
async def add_agreement(
    agreement_to_post: AgreementCreateDto,
    session: AsyncSession = Depends(get_session)
) -> AgreementDto:
    """
    If agreement is not available, then create agreement in origination with status NEW.
    :param agreement_to_post: agreement to add
    :param session: The connection session with DB
    :return: If agreement not in DB, create, then return agreement
    """
    agreement: AgreementDto = await create_agreement_db(agreement_to_post, session)

    return agreement


@agreement_router.post('/{agreement_id}', summary='Update status by id')
async def change_agreement_status(agreement_id: int, status: str,
                                  session: AsyncSession = Depends(get_session)) -> Response:
    """
    Change status for agreement by id.
    :param agreement_id: agreement to add
    :param status: new status
    :param session: The connection session with DB
    :return: If agreement not in DB, create, then return agreement
    """
    await change_agreement_status(agreement_id=agreement_id, new_status=status, session=session)

    return Response(media_type='text/plain', content='Статус обновлен.')
