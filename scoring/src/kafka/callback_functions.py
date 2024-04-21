import json
import logging
import os

import httpx
from fastapi import HTTPException

from common.kafka_managers.producer import send_message
from common.scoring_status import Status
from scoring.src.kafka.kafka_entites import kafka_producer_scoring_response
from scoring.src.models.dto import AgreementDto

host = os.getenv('PRODUCT_ENGINE_HOST')
port = os.getenv('PRODUCT_ENGINE_PORT')


async def scoring_request(msg):
    request_info = AgreementDto(**json.loads(msg.value.decode('ascii')))
    logging.info('START SCORING REQUEST')
    url = f'{host}:{port}/agreement/{request_info.person_id}'
    async with httpx.AsyncClient() as client:
        response = (await client.get(url))
        logging.info('SCORING RESPONSE: %s', response.json())
        if not response.is_success:
            raise HTTPException(status_code=response.status_code, detail=response.json())

    answer = True
    for agreement_json in response.json():
        logging.info('SCORING RESPONSE INFO: %s', agreement_json)
        agreement: AgreementDto = AgreementDto(
            person_id=agreement_json['person_id'],
            agreement_id=agreement_json['agreement_id'],
            status=agreement_json['status']
        )
        if agreement.agreement_id == request_info.agreement_id:
            continue
        if agreement.status != Status.CLOSED.value:
            answer = False
            break

    request_info.status = Status.APPROVED.value if answer else Status.REJECTED.value
    logging.info('SCORING RESPONSE: RESULT %s', request_info.json())
    topic = os.getenv('TOPIC_NAME_SCORING_RESPONSES')
    async with kafka_producer_scoring_response.session() as session:
        await send_message(session, topic, request_info.dict())
