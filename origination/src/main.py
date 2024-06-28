import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from origination.src.endpoints.agreement import agreement_router
from origination.src.kafka.kafka_entities import kafka_consumer_scoring_responses, kafka_producer_scoring_requests, \
    kafka_consumer_new_agreements, event_loop
from origination.src.kafka.new_agreements_callback import new_agreement_callback
from origination.src.kafka.scoring_response_callback import scoring_response_callback

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


@asynccontextmanager
async def lifespan(_app: FastAPI):
    topic = os.getenv('TOPIC_NAME_SCORING_RESPONSES')
    await kafka_consumer_scoring_responses.init_consumer(topic, scoring_response_callback)
    event_loop.create_task(kafka_consumer_scoring_responses.consume())

    topic = os.getenv('TOPIC_NAME_AGREEMENTS')
    logging.info('TOPIC INIT: %s', topic)
    await kafka_consumer_new_agreements.init_consumer(topic, new_agreement_callback)
    event_loop.create_task(kafka_consumer_new_agreements.consume())

    await kafka_producer_scoring_requests.init_producer()

    yield

    await kafka_consumer_scoring_responses.stop()
    await kafka_producer_scoring_requests.stop()
    await kafka_consumer_new_agreements.stop()


app = FastAPI(
    title='Origination API',
    summary='Documentation of Fintech Credits API - Origination',
    description='There will be some description of Fintech API',
    version='1.0.0',
    lifespan=lifespan
)

app.include_router(agreement_router)
