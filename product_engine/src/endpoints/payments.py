import os
from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from common.generic_repository import GenericRepository
from common.kafka_managers.producer import send_message
from product_engine.src.kafka.kafka_entites import kafka_producer_payments
from product_engine.src.models.dao import PaymentDao
from product_engine.src.models.dto import PaymentBaseDto, PaymentDto, PersonPaymentDto
from product_engine.src.models.session_maker import get_session

payment_router = APIRouter(prefix="/payment")


@payment_router.post('', summary='Create new payment')
async def create_payment(
    payment_to_post: PaymentBaseDto,
    session: AsyncSession = Depends(get_session)
) -> Response:
    """
    If payment is not available, then create new payment.
    :param payment_to_post: payment to create
    :param session: The connection session with DB
    """
    repository = GenericRepository(session, PaymentDao)
    payment: PaymentDao = (await repository.get_one_by_condition(
        PaymentDao.agreement_id == payment_to_post.agreement_id & PaymentDao.serial_nmb_payment == payment_to_post.serial_nmb_payment))

    if payment:
        raise HTTPException(status_code=409, detail='Такой платеж  уже существует')

    new_payment = PaymentDao(agreement_id=payment_to_post.agreement_id,
                             payment_dt=payment_to_post.payment_dt,
                             payment_amt_debt=payment_to_post.payment_amt_debt,
                             payment_amt_proc=payment_to_post.payment_amt_proc,
                             serial_nmb_payment=payment_to_post.serial_nmb_payment,
                             status=payment_to_post.serial_nmb_payment)

    await repository.save(new_payment)
    return Response(media_type='text/plain', content='Платеж успешно добавлен!')


@payment_router.get(
    's/{agreement_id}',
    response_model=list[PaymentDto],
    summary='Get list of payments by id of agreement'
)
async def get_payments_by_agreement_id(agreement_id: int,
                                       session: AsyncSession = Depends(get_session)) -> list[PaymentDto]:
    """
    :param agreement_id: id of agreement
    :param session: The connection session with DB
    :return: List of Json represented payments
    """
    payments: Sequence[PaymentDao] = (
        await GenericRepository(session, PaymentDao).get_all_by_condition(
            PaymentDao.agreement_id == agreement_id))

    return [payment.convert_to_dto() for payment in payments]


@payment_router.post(
    '/pay',
    summary='Make a payment'
)
async def make_payment(payment: PersonPaymentDto) -> Response:
    """
    :param payment: date, agreement_id, value of payment
    :return: Response
    """
    topic = os.getenv('TOPIC_NAME_RECIEVED_PAYMENT')
    async with kafka_producer_payments.session() as session_kafka:
        await send_message(session_kafka, topic, payment.model_dump())
    return Response(media_type='text/plain', content='Платеж принят.')
