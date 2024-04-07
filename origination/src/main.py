import asyncio
from typing import Sequence
import os
import httpx
from aiokafka import AIOKafkaConsumer
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager

from fastapi import FastAPI, Response

from common.scoring_status import Status
from common.generic_repository import GenericRepository
from origination.src.endpoints.agreement import agreement_router
from origination.src.models.dao import AgreementDao
from origination.src.models.session_maker import async_session

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    scheduler.start()
    scheduler.add_job(refresh_agreements, 'interval', seconds=15)
    event_loop.create_task(consume())
    yield
    await consumer.stop()
    scheduler.shutdown()


host = os.getenv('INTERNAL_HOST')
port = os.getenv('SCORING_PORT')


async def refresh_agreements():
    async with async_session() as session:
        async with session.begin():
            repository = GenericRepository(session, AgreementDao)
            agreements: Sequence[AgreementDao] = (
                await repository.get_all_by_params_and(['status', ], [Status.NEW.value, ])
            )
            for agreement in agreements:
                url = f'{host}:{port}/score_agreement'
                async with httpx.AsyncClient() as client:
                    response = await client.post(url, json=agreement.convert_to_dto().model_dump())
                    if response.status_code != 200:
                        continue  # skip
                    await repository.update_property(
                        ['agreement_id'],
                        [agreement.agreement_id],
                        'status',
                        Status.SCORING.value
                    )

    return Response(
        status_code=200,
        media_type='text/plain',
        content='Agreement to score job done'
    )


app = FastAPI(
    title='Origination API',
    summary='Documentation of Fintech Credits API - Origination',
    description='There will be some description of Fintech API',
    version='1.0.0',
    lifespan=lifespan
)

app.include_router(agreement_router)

event_loop = asyncio.get_event_loop()
kafka = os.getenv('KAFKA_INSTANCE')
produce_topic = os.getenv('TOPIC_NAME_AGREEMENTS')
consumer = AIOKafkaConsumer(produce_topic, bootstrap_servers=kafka, loop=event_loop)


async def consume():
    await consumer.start()
    try:
        print("start")
        while True:
            async for msg in consumer:
                print(msg)
    finally:
        await consumer.stop()
