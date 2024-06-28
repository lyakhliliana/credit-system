from sqlalchemy.ext.asyncio import AsyncSession

from common.generic_repository import GenericRepository
from product_engine.src.models.dao import AgreementDao
from product_engine.src.models.dto import AgreementDto


async def get_agreement_by_id(agreement_id: int, session: AsyncSession) -> AgreementDto:
    repository = GenericRepository(session, AgreementDao)
    agreement: AgreementDao = (await repository.get_one_by_condition(AgreementDao.agreement_id == agreement_id))
    if agreement is None:
        raise Exception('Заявки с указанным ID не существует')
    return agreement.convert_to_dto()
