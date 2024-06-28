import os
from typing import Sequence

from fastapi import Response

from common.generic_repository import GenericRepository
from common.kafka_managers.producer import send_message
from common.status import AgreementStatus
from origination.src.kafka.kafka_entities import kafka_producer_scoring_requests
from origination.src.models.dao import AgreementDao
from origination.src.models.session_maker import get_session

topic_scoring_request = os.getenv('TOPIC_NAME_SCORING_REQUESTS')


async def refresh_agreements():
    agreements: Sequence[AgreementDao] = None
    async for session in get_session():
        repository = GenericRepository(session, AgreementDao)
        agreements = (
            await repository.get_all_by_condition((AgreementDao.status == AgreementStatus.NEW.value)))

    for agreement in agreements:
        async with kafka_producer_scoring_requests.session() as session_kafka:
            await send_message(
                session_kafka, topic_scoring_request,
                agreement.convert_to_dto().model_dump()
            )

    async for session in get_session():
        repository = GenericRepository(session, AgreementDao)
        await repository.update_property(
            ['agreement_id'],
            [agreement.agreement_id],
            'status',
            AgreementStatus.SCORING.value
        )

    return Response(
        status_code=200,
        media_type='text/plain',
        content='Agreement send to scoring through kafka.'
    )
