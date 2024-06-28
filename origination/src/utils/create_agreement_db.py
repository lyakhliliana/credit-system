import logging

from sqlalchemy.ext.asyncio import AsyncSession

from common.generic_repository import GenericRepository
from common.status import AgreementStatus
from origination.src.models.dao import AgreementDao
from origination.src.models.dto import AgreementDto, AgreementCreateDto


async def create_agreement_db(agreement_to_post: AgreementCreateDto, session: AsyncSession) -> AgreementDto:
    repository = GenericRepository(session, AgreementDao)
    agreement: AgreementDao = (await repository.get_one_by_condition(
        AgreementDao.agreement_id == agreement_to_post.agreement_id))

    if not agreement:
        agreement = AgreementDao(
            agreement_id=agreement_to_post.agreement_id,
            person_id=agreement_to_post.person_id,
            status=AgreementStatus.NEW.value
        )
        await repository.save(agreement)

    return agreement.convert_to_dto()
