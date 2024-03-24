from typing import Sequence

import httpx
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from common.generic_repository import GenericRepository
from origination.src.models.dao import AgreementDao
from origination.src.models.dto import AgreementDto, AgreementCreateDto
from origination.src.models.session_maker import get_session, async_session
from common.scoring_status import Status

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(_app: FastAPI):
    scheduler.start()
    scheduler.add_job(refresh_agreements, 'interval', seconds=15)
    yield
    scheduler.shutdown()


host = 'http://172.29.176.1'


async def refresh_agreements():
    async with async_session() as session:
        async with session.begin():
            repository = GenericRepository(session, AgreementDao)
            agreements: Sequence[AgreementDao] = (
                await repository.get_all_by_params_and(['status', ], [Status.NEW.value, ])
            )
            for agreement in agreements:
                url = f"{host}:50/score_agreement"
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


@app.get(
    '/agreement/{agreement_id}',
    response_model=AgreementDto,
    summary='Get the specified agreement'
)
async def get_agreement_by_id(agreement_id: int, session: AsyncSession = Depends(get_session)) -> AgreementDto:
    """
    :param agreement_id: id of agreement to retrieve
    :param session: The connection session with DB
    :return: if agreement id is available, then retrieve product info, else Not Found
    """
    repository = GenericRepository(session, AgreementDao)
    agreement_dao: AgreementDao = (await repository.get_one_by_params(['agreement_id'], [agreement_id]))
    if agreement_dao is None:
        raise HTTPException(status_code=404, detail='Not found')
    return AgreementDto(agreement_id=agreement_dao.agreement_id, status=agreement_dao.status)


@app.get(
    '/new_agreements',
    response_model=list[AgreementDto],
    summary='Get list of new agreements'
)
async def get_new_agreements(session: AsyncSession = Depends(get_session)) -> list[AgreementDto]:
    """
    Retrieve all new agreements.
    :param session: The connection session with DB
    :return: List of Json represented agreements with status NEW
    """
    agreements: Sequence[AgreementDao] = (await GenericRepository(session, AgreementDao).get_all_by_params_and(
        ['status', ],
        [Status.NEW.value, ]
    ))
    if len(agreements) == 0:
        raise HTTPException(status_code=404, detail='Not found')
    return [agreement.convert_to_dto() for agreement in agreements]


@app.get(
    '/scored_agreements',
    response_model=list[AgreementDto],
    summary='Get list of scored agreements'
)
async def get_scored_agreements(session: AsyncSession = Depends(get_session)) -> list[AgreementDto]:
    """
    Retrieve all scored agreements.
    :param session: The connection session with DB
    :return: List of Json represented agreements with status REJECT and APPROVED
    """
    agreements: Sequence[AgreementDao] = (await GenericRepository(session, AgreementDao).get_all_by_params_or(
        ['status', 'status', ],
        [Status.REJECTED.value, Status.APPROVED.value, ]
    ))
    if len(agreements) == 0:
        raise HTTPException(status_code=404, detail='Not found')
    return [agreement.convert_to_dto() for agreement in agreements]


@app.post('/agreement',
          response_model=AgreementDto,
          summary='Add new agreement')
async def add_agreement(
        agreement_to_post: AgreementCreateDto,
        session: AsyncSession = Depends(get_session)
):
    """
    If agreement is not available, then create agreement in origination with status NEW.
    :param agreement_to_post: agreement to add
    :param session: The connection session with DB
    :return: If agreement not in DB, create, then return agreement
    """
    repository = GenericRepository(session, AgreementDao)
    agreement: AgreementDao = (await repository.get_one_by_params(
        ['agreement_id'],
        [agreement_to_post.agreement_id]
    ))
    if agreement:
        return agreement.convert_to_dto()

    agreement_n = AgreementDao(agreement_id=agreement_to_post.agreement_id, status=Status.NEW.value)
    await repository.save(agreement_n)
    return agreement_n.convert_to_dto()
