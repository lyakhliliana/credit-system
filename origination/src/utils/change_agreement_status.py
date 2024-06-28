from sqlalchemy.ext.asyncio import AsyncSession

from common.generic_repository import GenericRepository
from origination.src.models.dao import AgreementDao


async def change_agreement_status(agreement_id: int, new_status: str, session: AsyncSession):
    repository = GenericRepository(session, AgreementDao)
    agreement: AgreementDao = (await repository.get_one_by_condition(AgreementDao.agreement_id == agreement_id))
    if agreement is None:
        raise Exception('Заявки с указанным ID не существует')

    await repository.update_property(
        ['agreement_id'],
        [agreement.agreement_id],
        'status',
        new_status)
