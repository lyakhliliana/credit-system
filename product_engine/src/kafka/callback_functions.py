import json

from common.generic_repository import GenericRepository
from common.status import PaymentStatus, AgreementStatus
from product_engine.src.models.dao import AgreementDao, PaymentDao
from product_engine.src.models.dto import KafkaAgreementDto, AgreementDto
from product_engine.src.models.session_maker import get_session
from product_engine.src.utils.payment_math import calc_periods


async def _get_agreement_by_id(agreement_id) -> AgreementDto:
    async for session in get_session():
        agreement = (await GenericRepository(session, AgreementDao).get_one_by_condition(
            AgreementDao.agreement_id == agreement_id)).convert_to_dto()
        return agreement


async def _save_payment_schedule(periods, agreement_id):
    async for session in get_session():
        for i in range(1, len(periods) + 1):
            payment_to_post = PaymentDao(agreement_id=agreement_id,
                                         payment_dt=periods[i]['payment_dt'],
                                         payment_amt_debt=periods[i]['payment_amt_debt'],
                                         payment_amt_proc=periods[i]['payment_amt_proc'],
                                         serial_nmb_payment=i,
                                         status=PaymentStatus.FUTURE.value)
            repository = GenericRepository(session, PaymentDao)
            await repository.save(payment_to_post)


async def _change_agreement_status(agreement_id, status: str):
    async for session in get_session():
        repository = GenericRepository(session, AgreementDao)
        await repository.update_property(['agreement_id'], [agreement_id], 'status',
                                         status)


async def make_payment_schedule(msg):
    request_info = KafkaAgreementDto(**json.loads(msg.value.decode('ascii')))

    if request_info.status != AgreementStatus.APPROVED.value:
        await _change_agreement_status(request_info.agreement_id, AgreementStatus.CLOSED.value)
        return

    agreement = await _get_agreement_by_id(request_info.agreement_id)

    rate = agreement.interest
    n_per = agreement.load_term
    principal_amount = agreement.principal_amount
    agreement_dttm = agreement.agreement_dttm
    date = agreement_dttm.date()

    payment_periods = calc_periods(rate, n_per, principal_amount, date)

    await _save_payment_schedule(payment_periods, request_info.agreement_id)

    await _change_agreement_status(request_info.agreement_id, AgreementStatus.ACTIVE.value)
