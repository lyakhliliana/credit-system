import json
import os
from datetime import datetime
import random

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from common.generic_repository import GenericRepository
from common.status import AgreementStatus
from product_engine.src.models.dao import AgreementDao, PersonDao
from product_engine.src.models.dao import ProductDao
from product_engine.src.models.dto import ApplicationCreateDto
from product_engine.src.models.session_maker import get_session
from product_engine.src.utils.get_kafka_producer import AgreementProducer, get_producer
from product_engine.src.utils.valid_transaction_check import check_valid_agreement_condition

application_router = APIRouter(prefix="/application")


@application_router.post('', summary='Clients request to create agreement')
async def application_request_create(
        application_to_post: ApplicationCreateDto,
        session: AsyncSession = Depends(get_session),
        kafka_producer: AgreementProducer = Depends(get_producer)
):
    """
    Create new agreement of person.
    :param kafka_producer:
    :param application_to_post: agreement data
    :param session: The connection session with DB
    :return: Agreement id, otherwise 400, 409
    """
    repository_product = GenericRepository(session, ProductDao)
    product: ProductDao = (await repository_product.get_one_by_params(
        ['code'],
        [application_to_post.product_code]
    ))

    if product is None:
        raise HTTPException(status_code=400, detail='Продукт с таким кодом не существует')

    repository_person = GenericRepository(session, PersonDao)
    person: PersonDao = (await repository_person.get_one_by_params(
        ['first_nm', 'last_nm', 'middle_nm', 'birth_dt', 'passport_no', 'email'],
        [application_to_post.first_name, application_to_post.second_name,
         application_to_post.third_name,
         datetime.strptime(application_to_post.birthday, '%d.%m.%Y'),
         application_to_post.passport_number,
         application_to_post.email]
    ))
    if person:
        person_n = person
    else:
        person_n = PersonDao(
            first_nm=application_to_post.first_name,
            last_nm=application_to_post.second_name,
            middle_nm=application_to_post.third_name,
            birth_dt=datetime.strptime(application_to_post.birthday, '%d.%m.%Y'),
            passport_no=application_to_post.passport_number,
            email=application_to_post.email,
            mobile_phone_no=application_to_post.phone,
            monthly_income_amt=int(application_to_post.salary)
        )
        await repository_person.save(person_n)

    repository_agreement = GenericRepository(session, AgreementDao)
    agreement: AgreementDao = (await repository_agreement.get_one_by_params([
        'person_id',
        'product_code',
        'load_term',
        'interest'
    ],
        [
            person_n.person_id,
            application_to_post.product_code,
            application_to_post.term,
            application_to_post.interest
        ]
    ))
    if agreement is not None:
        return agreement.agreement_id

    origination_amt = random.random() * (float(product.max_origination_amount) - float(product.min_origination_amount))
    origination_amt += float(product.min_origination_amount)

    agreement_n = AgreementDao(
        product_code=application_to_post.product_code,
        person_id=person_n.person_id,
        load_term=application_to_post.term,
        principal_amount=application_to_post.disbursement_amount + origination_amt,
        interest=application_to_post.interest,
        origination_amount=origination_amt,
        agreement_dttm=datetime.now(),
        status=AgreementStatus.NEW.value
    )

    if not check_valid_agreement_condition(product=product, agreement=agreement_n):
        raise HTTPException(status_code=400, detail='Данные договора не соответствуют продукту')

    await repository_agreement.save(agreement_n)

    return agreement_n.agreement_id


@application_router.post('/{agreement_id}/close', summary='Clients request to cancel agreement')
async def application_request_cancel(agreement_id: int, session: AsyncSession = Depends(get_session)):
    repository = GenericRepository(session, AgreementDao)
    agreement: AgreementDao = (await repository.get_one_by_params(['agreement_id'], [agreement_id]))
    if agreement is None:
        raise HTTPException(status_code=404, detail='Заявка с указанным ID не существует')

    await repository.update_property(
        ['agreement_id'],
        [agreement.agreement_id],
        'status',
        AgreementStatus.CLOSED.value
    )

    return Response(
        status_code=200,
        media_type='text/plain',
        content='Заявка с указанным ID была успешно закрыта'
    )
