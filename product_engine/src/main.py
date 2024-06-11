import os
from contextlib import asynccontextmanager
from typing import Sequence

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI, Response

from common.kafka_managers.producer import send_message
from common.scoring_status import Status
from common.generic_repository import GenericRepository
from product_engine.src.kafka.kafka_entites import kafka_producer_agreements
from product_engine.src.endpoints.agreement import agreement_router
from product_engine.src.endpoints.application import application_router
from product_engine.src.endpoints.product import product_router
from product_engine.src.models.dao import AgreementDao
from product_engine.src.models.session_maker import async_session

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await kafka_producer_agreements.init_producer()

    scheduler.start()
    scheduler.add_job(refresh_agreements, 'interval', seconds=15)

    yield
    kafka_producer_agreements.stop()
    scheduler.shutdown()


async def refresh_agreements():
    async with async_session() as session:
        async with session.begin():
            repository = GenericRepository(session, AgreementDao)
            agreements: Sequence[AgreementDao] = (
                await repository.get_all_by_params_and(['status', ], [Status.NEW.value, ])
            )
            topic = os.getenv('TOPIC_NAME_AGREEMENTS')
            for agreement in agreements:
                async with kafka_producer_agreements.session() as session_kafka:
                    await send_message(
                        session_kafka,
                        topic,
                        agreement.convert_to_dto().model_dump(include={'agreement_id', 'person_id'})
                    )

                await repository.update_property(
                    ['agreement_id'],
                    [agreement.agreement_id],
                    'status',
                    Status.SCORING.value
                )
    return Response(
        status_code=200,
        media_type='text/plain',
        content='Agreement send to origination'
    )


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

