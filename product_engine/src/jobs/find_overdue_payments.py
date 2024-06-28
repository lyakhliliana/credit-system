import datetime
import os
from typing import Sequence

from fastapi import Response

from common.generic_repository import GenericRepository
from common.kafka_managers.producer import send_message
from common.status import PaymentStatus
from product_engine.src.kafka.kafka_entites import kafka_producer_overdue_payments
from product_engine.src.models.dao import PaymentDao, AgreementDao
from product_engine.src.models.dto import KafkaOverduePayment
from product_engine.src.models.session_maker import async_session


async def find_overdue_payments():
    async with async_session() as session:
        async with session.begin():

            repository_payment = GenericRepository(session, PaymentDao)
            payments: Sequence[PaymentDao] = (
                await repository_payment.get_all_by_params_and(['status', ], [PaymentStatus.FUTURE.value, ])
            )

            topic = os.getenv('TOPIC_NAME_OVERDUE_PAYMENTS')
            cur_date_str = os.getenv('TEST_DATE_OVERDUE_PAYMENTS', default=datetime.date.today().isoformat())
            cur_date = datetime.datetime.strptime(cur_date_str, '%Y-%m-%d')

            for payment in payments:

                if payment.payment_dt <= cur_date.date():
                    continue

                repository_agreement = GenericRepository(session, AgreementDao)
                agreement: AgreementDao = (
                    await repository_agreement.get_one_by_params(['agreement_id', ], [payment.agreement_id])
                )

                async with kafka_producer_overdue_payments.session() as session_kafka:
                    kafka_payment = KafkaOverduePayment(customer_id=agreement.person_id,
                                                        agreement_id=agreement.agreement_id,
                                                        overdue_date=payment.payment_dt,
                                                        payment=payment.payment_amt_debt + payment.payment_amt_proc)
                    await send_message(session_kafka, topic, kafka_payment.dict())

                await repository_payment.update_property(['payment_id'], [payment.payment_id],
                                                         'status', PaymentStatus.OVERDUE.value)

    return Response(status_code=200, media_type='text/plain', content='Payments checked for late')
