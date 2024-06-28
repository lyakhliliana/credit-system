import os
from contextlib import asynccontextmanager

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI

from product_engine.src.endpoints.agreement import agreement_router
from product_engine.src.endpoints.application import application_router
from product_engine.src.endpoints.payments import payment_router
from product_engine.src.endpoints.product import product_router
from product_engine.src.jobs.find_overdue_payments import find_overdue_payments
from product_engine.src.jobs.refresh_agreements import refresh_agreements
from product_engine.src.kafka.get_recieved_payment_callback import get_recieved_payment
from product_engine.src.kafka.make_payment_schedule_callback import make_payment_schedule
from product_engine.src.kafka.kafka_entites import event_loop, kafka_producer_overdue_payments, \
    kafka_consumer_payment_recieved, kafka_producer_payments
from product_engine.src.kafka.kafka_entites import kafka_producer_agreements, kafka_consumer_scoring_responses

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await kafka_producer_agreements.init_producer()
    await kafka_producer_overdue_payments.init_producer()
    await kafka_producer_payments.init_producer()

    topic = os.getenv('TOPIC_NAME_SCORING_RESPONSES')
    await kafka_consumer_scoring_responses.init_consumer(topic, make_payment_schedule)
    event_loop.create_task(kafka_consumer_scoring_responses.consume())

    topic = os.getenv('TOPIC_NAME_RECIEVED_PAYMENT')
    await kafka_consumer_payment_recieved.init_consumer(topic, get_recieved_payment)
    event_loop.create_task(kafka_consumer_payment_recieved.consume())

    scheduler.start()
    scheduler.add_job(refresh_agreements, 'interval', seconds=15)
    scheduler.add_job(find_overdue_payments, 'interval', seconds=30)

    yield
    kafka_producer_agreements.stop()
    kafka_producer_overdue_payments.stop()
    kafka_producer_payments.stop()
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
