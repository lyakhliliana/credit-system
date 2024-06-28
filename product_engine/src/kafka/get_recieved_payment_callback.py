import json

from common.generic_repository import GenericRepository
from product_engine.src.models.dao import PaymentDao
from product_engine.src.models.dto import KafkaPaymentRecievedDto, AgreementDto
from product_engine.src.models.session_maker import get_session
from product_engine.src.utils.get_agreement_by_id import get_agreement_by_id


async def get_recieved_payment(msg):
    request_info = KafkaPaymentRecievedDto(**json.loads(msg.value.decode('ascii')))
    agreement: AgreementDto = None
    async for session in get_session():
        agreement = await get_agreement_by_id(request_info.agreement_id, session)

    payments: list[PaymentDao] = []
    async for session in get_session():
        repository = GenericRepository(session, PaymentDao)
        payments: list[PaymentDao] = (await repository.get_one_by_condition(
            (PaymentDao.agreement_id == agreement.agreement_id)))
