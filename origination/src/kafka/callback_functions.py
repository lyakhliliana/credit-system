import logging
import json
import os

import httpx
from fastapi import HTTPException

from common.kafka_managers.producer import send_message
from common.scoring_status import Status
from origination.src.kafka.kafka_entities import kafka_producer_scoring_requests
from origination.src.models.dto import AgreementDto, AgreementCreateDto

host = os.getenv('ORIGINATION_HOST')
port = os.getenv('ORIGINATION_PORT')
topic = os.getenv('TOPIC_NAME_SCORING_REQUESTS')


async def _change_agreement_status(agreement_id, status_cd):
    async with httpx.AsyncClient() as client:
        # http://localhost:40/agreement/1?status=SCORING
        url = f'{host}:{port}/agreement/{agreement_id}?status={status_cd}'
        logging.info('ORIGINATION: CALLBACK CHANGE: TRYING TO POST')
        response = (await client.post(url))  # , json=dict(agreement_id=agreement_id, status=status_cd, )))
        logging.info('ORIGINATION: CALLBACK CHANGE: RESPONSE %s', response.text)
        if not response.is_success:
            raise HTTPException(status_code=response.status_code, detail=response.json())


async def scoring_response_callback(msg):
    logging.info('ORIGINATION: CALLBACK SCORING: START')
    result = AgreementDto(**json.loads(msg.value.decode('ascii')))
    logging.info('ORIGINATION: CALLBACK SCORING: RESULT: %s', result)
    logging.info('ORIGINATION: CALLBACK SCORING: TRYING TO POST')
    if result.status == Status.APPROVED.value:
        await _change_agreement_status(result.agreement_id, status_cd=Status.APPROVED.value)
    else:
        await _change_agreement_status(result.agreement_id, status_cd=Status.CLOSED.value)


async def create_application_callback(msg):
    logging.info('ORIGINATION: CALLBACK APPLICATION: START')
    result = AgreementCreateDto(**json.loads(msg.value.decode('ascii')))
    logging.info('ORIGINATION: CALLBACK APPLICATION: RESULT %s', result)
    url = f'{host}:{port}/agreement'
    async with httpx.AsyncClient() as client:
        logging.info('ORIGINATION: CALLBACK APPLICATION: TRYING TO POST %s', result.model_dump())
        response = (await client.post(url, json=result.model_dump()))
        logging.info('ORIGINATION: CALLBACK APPLICATION: RESPONSE %s', response.json())
        tmp: AgreementDto = AgreementDto(**response.json())
        if response.is_success:
            logging.info('ORIGINATION: CALLBACK APPLICATION: RESPONSE: success')
            async with kafka_producer_scoring_requests.session() as session:
                logging.info('ORIGINATION: CALLBACK APPLICATION: SENT MESSAGE')
                await send_message(session, topic, tmp.dict())
        else:
            raise HTTPException(status_code=response.status_code, detail=response.json())
    logging.info('ORIGINATION: CALLBACK APPLICATION: TRYING TO POST')
    await _change_agreement_status(tmp.agreement_id, status_cd=Status.SCORING.value)
