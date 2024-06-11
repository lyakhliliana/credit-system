import asyncio
import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Response

from scoring.src.kafka.callback_functions import scoring_request
from scoring.src.kafka.kafka_entites import kafka_consumer_scoring_requests, kafka_producer_scoring_response, event_loop
from scoring.src.models.dto import AgreementDto

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    topic = os.getenv('TOPIC_NAME_SCORING_REQUESTS')
    await kafka_consumer_scoring_requests.init_consumer(topic, scoring_request)
    await kafka_producer_scoring_response.init_producer()
    event_loop.create_task(kafka_consumer_scoring_requests.consume())
    yield

    await kafka_consumer_scoring_requests.stop()
    await kafka_producer_scoring_response.stop()


app = FastAPI(
    title='Scoring API',
    summary='Documentation of Fintech Credits API - Scoring',
    description='There will be some description of Fintech API',
    version='1.0.0',
    lifespan=lifespan
)


@app.post('/score_agreement',
          summary='Make agreement scored')
async def score_agreement(_: AgreementDto):
    """
    Make agreement scored
    :param _: agreement to score
    :return: stub
    """
    return Response(
        status_code=200,
        media_type='text/plain',
        content='Stub'
    )
