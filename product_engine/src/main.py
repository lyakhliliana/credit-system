import random
from datetime import datetime
from typing import Sequence
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from database.generic_repository import GenericRepository
from database.http_output import JsonBeautify
from product_engine.src.models.dao import ProductDao, PersonDao, AgreementDao
from product_engine.src.models.session_maker import get_session
from product_engine.src.models.dto import ProductBaseDto, ProductCreateDto, ApplicationCreateDto, AgreementDto, \
    ProductDto
from product_engine.src.utils.valid_transaction_check import check_valid_agreement_condition

app = FastAPI(
    title='PE API',
    summary='Documentation of Fintech Credits API',
    description='There will be some description of Fintech API',
    version='1.0.0',
)


@app.get(
    '/product',
    response_model=list[ProductDto],
    response_class=JsonBeautify,
    summary='Get list of available products'
)
async def get_all_products(session: AsyncSession = Depends(get_session)) -> list[ProductDto]:
    """
    Retrieve all products.
    :param session: The connection session with DB
    :return: List of Json represented products
    """
    products: Sequence[ProductDao] = (await GenericRepository(session, ProductDao).get_all())
    return [product.convert_to_dto() for product in products]


@app.get(
    '/product/{code}',
    response_model=ProductDto,
    response_class=JsonBeautify,
    summary='Get the specified product'
)
async def get_product(code: str, session: AsyncSession = Depends(get_session)) -> ProductDto:
    """

    :param code: Code of product to retrieve
    :param session: The connection session with DB
    :return: if product code is available, then retrieve product info, else Not Found
    """
    product: ProductDao = (await GenericRepository(session, ProductDao).get_one_by_params(['code'], [code]))
    if product is None:
        raise HTTPException(status_code=404, detail='Not found')
    return product.convert_to_dto()


@app.get(
    '/new_agreements/',
    response_model=list[AgreementDto],
    response_class=JsonBeautify,
    summary='Get the agreements with status NEW'
)
async def get_new_agreements(session: AsyncSession = Depends(get_session)) -> list[AgreementDto]:
    """
    :param session: The connection session with DB
    :return: list of agreements with status NEW
    """
    agreements: AgreementDao = (
        await GenericRepository(session, AgreementDao).get_all_by_params_and(['status'], ['NEW']))
    return [agreement.convert_to_dto() for agreement in agreements]


@app.post('/product', summary='Create new product')
async def set_product(
        product_to_post: ProductCreateDto,
        session: AsyncSession = Depends(get_session)
):
    """
    If product is not available, then create new product.
    :param product_to_post: product to create
    :param session: The connection session with DB
    :return: If product is not available, then return 200, otherwise raise error 409, 422
    """
    repository = GenericRepository(session, ProductDao)
    product: ProductDao = (await repository.get_one_by_params(['code'], [product_to_post.code]))
    if product:
        raise HTTPException(status_code=409, detail='Продукт с таким кодом уже существует')
    try:
        product_n = ProductDao(
            code=product_to_post.code,
            title=product_to_post.title,
            version=product_to_post.version,
            min_load_term=product_to_post.min_load_term,
            max_load_term=product_to_post.max_load_term,
            min_principal_amount=product_to_post.min_principal_amount,
            max_principal_amount=product_to_post.max_principal_amount,
            min_interest=product_to_post.min_interest,
            max_interest=product_to_post.max_interest,
            min_origination_amount=product_to_post.min_origination_amount,
            max_origination_amount=product_to_post.max_origination_amount
        )
    except SQLAlchemyError as ex:
        raise HTTPException(status_code=422, detail=f'Неверные данные, {ex}!')

    await repository.save(product_n)
    return Response(
        media_type='text/plain',
        content='Успешно добавлен!'
    )


@app.post('/application', summary='Clients request to create agreement')
async def application_request_create(
        application_to_post: ApplicationCreateDto,
        session: AsyncSession = Depends(get_session)
):
    """
    Create new agreement of person.
    :param application_to_post: agreement data
    :param session: The connection session with DB
    :return: Agreement id, otherwise 400, 409
    """
    repository_product = GenericRepository(session, ProductDao)
    product: ProductDao = (await repository_product.get_one_by_params(['code'], [application_to_post.product_code]))
    if product is None:
        raise HTTPException(status_code=400, detail="Продукт с таким кодом не существует")

    repository_person = GenericRepository(session, PersonDao)
    person: PersonDao = (
        await repository_person.get_one_by_params(
            ['first_nm', 'last_nm', 'middle_nm', 'birth_dt', 'passport_no', 'email'],
            [application_to_post.first_name, application_to_post.second_name,
             application_to_post.third_name,
             datetime.strptime(application_to_post.birthday, '%d.%m.%Y'),
             application_to_post.passport_number,
             application_to_post.email]))
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
        status="NEW"
    )

    if not check_valid_agreement_condition(product=product, agreement=agreement_n):
        raise HTTPException(status_code=400, detail="Данные договора не соответствуют продукту")

    await repository_agreement.save(agreement_n)
    return agreement_n.agreement_id


@app.post('/application/{agreement_id}/close', summary='Clients request to cancel agreement')
async def application_request_cancel(
        agreement_id: int | UUID,
        session: AsyncSession = Depends(get_session)
):
    repository = GenericRepository(session, AgreementDao)
    agreement: AgreementDao = (await repository.get_one_by_params(['agreement_id'], [agreement_id]))
    if agreement is None:
        raise HTTPException(status_code=404, detail="Заявка с указанным ID не существует")

    await repository.update_property(
        ['agreement_id'],
        [agreement.agreement_id],
        'status',
        'CLOSED'
    )

    return Response(
        status_code=200,
        media_type='text/plain',
        content='Заявка с указанным ID была успешно закрыта'
    )


@app.delete('/product/{code}', summary='Delete product')
async def delete_product(code: str, session: AsyncSession = Depends(get_session)):
    """
    Delete product by product code.
    :param code: code of product
    :param session: The connection session with DB
    :return: response 204
    """
    repository = GenericRepository(session, ProductDao)
    product: ProductDao = (await repository.get_one_by_params(['code'], [code]))
    if product:
        await repository.delete(code)
    return Response(
        status_code=204,
        media_type='text/plain',
        content='Продукт с указанным кодом был успешно удален!'
    )

# if __name__ == "__main__":
#     uvicorn.run("main:app", port=80, log_level="info")
