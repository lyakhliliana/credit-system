from typing import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from common.generic_repository import GenericRepository
from common.scoring_status import Status
from product_engine.src.models.dao import AgreementDao
from product_engine.src.models.dto import AgreementDto
from product_engine.src.models.session_maker import get_session

agreement_router = APIRouter(prefix="/agreement")


@agreement_router.get(
    '/new',
    response_model=list[AgreementDto],
    summary='Get the agreements with status NEW'
)
async def get_new_agreements(session: AsyncSession = Depends(get_session)) -> list[AgreementDto]:
    """
    :param session: The connection session with DB
    :return: list of agreements with status NEW
    """
    agreements: Sequence[AgreementDao] = (
        await GenericRepository(session, AgreementDao).get_all_by_params_and(
            ['status'],
            [Status.NEW.value]
        )
    )
    return [agreement.convert_to_dto() for agreement in agreements]
