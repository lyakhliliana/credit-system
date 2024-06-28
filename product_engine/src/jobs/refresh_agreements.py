import os
from typing import Sequence

from fastapi import Response

from common.generic_repository import GenericRepository
from common.kafka_managers.producer import send_message
from common.status import AgreementStatus
from product_engine.src.kafka.kafka_entites import kafka_producer_agreements
from product_engine.src.models.dao import AgreementDao
from product_engine.src.models.session_maker import async_session


async def refresh_agreements():
    async with async_session() as session:
        async with session.begin():
            repository = GenericRepository(session, AgreementDao)
            agreements: Sequence[AgreementDao] = (
                await repository.get_all_by_condition(AgreementDao.status == AgreementStatus.NEW.value))

            topic = os.getenv('TOPIC_NAME_AGREEMENTS')
            for agreement in agreements:
                async with kafka_producer_agreements.session() as session_kafka:
                    await send_message(
                        session_kafka, topic,
                        agreement.convert_to_dto().model_dump(include={'agreement_id', 'person_id'})
                    )

                await repository.update_property(
                    ['agreement_id'],
                    [agreement.agreement_id],
                    'status',
                    AgreementStatus.SCORING.value
                )
    return Response(
        status_code=200,
        media_type='text/plain',
        content='Agreement send to origination through kafka.'
    )
