import json
import logging
import os

from common.kafka_managers.producer import send_message
from common.status import AgreementStatus
from origination.src.kafka.kafka_entities import kafka_producer_scoring_requests
from origination.src.models.dto import AgreementCreateDto, AgreementDto
from origination.src.models.session_maker import get_session
from origination.src.utils.change_agreement_status import change_agreement_status
from origination.src.utils.create_agreement_db import create_agreement_db

topic_scoring_request = os.getenv('TOPIC_NAME_SCORING_REQUESTS')


async def new_agreement_callback(msg):
    request_data = AgreementCreateDto(**json.loads(msg.value.decode('ascii')))
    agreement: AgreementDto
    async for session in get_session():
        agreement = await create_agreement_db(request_data, session)

    if agreement.status in (AgreementStatus.APPROVED.value, AgreementStatus.REJECTED.value):
        async for session in get_session():
            await change_agreement_status(agreement_id=agreement.agreement_id,
                                          new_status=agreement.status,
                                          session=session)

    async with kafka_producer_scoring_requests.session() as session:
        await send_message(session, topic_scoring_request, agreement.dict())

    async for session in get_session():
        await change_agreement_status(agreement_id=agreement.agreement_id, new_status=AgreementStatus.SCORING.value,
                                      session=session)
