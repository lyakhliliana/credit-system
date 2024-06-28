import json
import logging
from datetime import datetime

from common.generic_repository import GenericRepository
from common.status import PaymentStatus
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
        payments = (await repository.get_all_by_condition(
            (PaymentDao.agreement_id == agreement.agreement_id) & (PaymentDao.status == PaymentStatus.FUTURE.value)))
    payments.sort(key=lambda x: x.serial_nmb_payment)

    if not payments:
        raise Exception("No future payments.")

    for payment in payments:
        payment = payment.convert_to_dto()
        logging.info("---------------------------" + payment.__str__())
        if (datetime.strptime(request_info.date, '%Y-%m-%d').date() <= payment.payment_dt) and (
            request_info.payment + payment.payment_amt_debt + payment.payment_amt_proc < 0.5):

            async for session in get_session():
                repository = GenericRepository(session, PaymentDao)
                await repository.update_property(
                    ['payment_id'],
                    [payment.payment_id],
                    'status',
                    PaymentStatus.PAID.value)
