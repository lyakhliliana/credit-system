import os
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

from product_engine.src.endpoints.agreement import agreement_router
from product_engine.src.endpoints.application import application_router
from product_engine.src.endpoints.payments import payment_router
from product_engine.src.endpoints.product import product_router
from product_engine.src.jobs.refresh_agreements import refresh_agreements
from product_engine.src.kafka.callback_functions import make_payment_schedule
from product_engine.src.kafka.kafka_entites import event_loop
from product_engine.src.kafka.kafka_entites import kafka_producer_agreements, kafka_consumer_scoring_responses

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await kafka_producer_agreements.init_producer()

    topic = os.getenv('TOPIC_NAME_SCORING_RESPONSES')
    await kafka_consumer_scoring_responses.init_consumer(topic, make_payment_schedule)
    event_loop.create_task(kafka_consumer_scoring_responses.consume())

    scheduler.start()
    scheduler.add_job(refresh_agreements, 'interval', seconds=15)

    yield
    kafka_producer_agreements.stop()
    kafka_consumer_scoring_responses.stop()
    scheduler.shutdown()


app = FastAPI(
    title='PE API',
    summary='Documentation of Fintech Credits API',
    description='There will be some description of Fintech API',
    version='1.0.0',
    lifespan=lifespan
)

app.include_router(product_router)
app.include_router(application_router)
app.include_router(agreement_router)
app.include_router(payment_router)
