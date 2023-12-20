import random
from datetime import datetime
from typing import Sequence

from fastapi import Depends, FastAPI, HTTPException, Response
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from product_engine.src.database_models.dao import ProductDao, PersonDao, AgreementDao
from product_engine.src.database_models.database import get_session, Repository
from product_engine.src.database_models.dto import ProductBaseDto, ProductCreateDto, AgreementCreateDto

from product_engine.src.utils.http_output import JsonBeautify
from product_engine.src.utils.transaction_check import check_valid_agreement_condition

app = FastAPI(
    title='Fintech API',
    summary='Documentation of Fintech Credits API',
    description='There will be some description of Fintech API',
    version='1.0.0',
)


@app.get(
    '/product',
    response_model=list[ProductBaseDto],
    response_class=JsonBeautify,
    summary='Get list of available products'
)
async def get_all_products(session: AsyncSession = Depends(get_session)) -> list[ProductBaseDto]:
    """
    Retrieve all products.
    :param session: The connection session with DB
    :return: List of Json represented products
    """
    # products: Sequence[ProductDao] = (await session.execute(select(ProductDao))).scalars().all()
    products: Sequence[ProductDao] = (await Repository.get_all(ProductDao, session)).all()
    return [ProductBaseDto(
        code=product.code,
        title=product.title,
        version=product.version,
        min_load_term=product.min_load_term,
        max_load_term=product.max_load_term,
        min_principal_amount=product.min_principal_amount,
        max_principal_amount=product.max_principal_amount,
        min_interest=product.min_interest,
        max_interest=product.max_interest,
        min_origination_amount=product.min_origination_amount,
        max_origination_amount=product.max_origination_amount,
    ) for product in products]


@app.get(
    '/product/{code}',
    response_model=ProductBaseDto,
    response_class=JsonBeautify,
    summary='Get the specified product'
)
async def get_product(code: str, session: AsyncSession = Depends(get_session)) -> ProductBaseDto:
    """

    :param code: Code of product to retrieve
    :param session: The connection session with DB
    :return: if product code is available, then retrieve product info, else Not Found
    """
    product: ProductDao = (await Repository.get(ProductDao, session, ['code'], [code])).one_or_none()
    if product is None:
        raise HTTPException(status_code=404, detail='Not found')
    return ProductBaseDto(
        code=product.code,
        title=product.title,
        version=product.version,
        min_load_term=product.min_load_term,
        max_load_term=product.max_load_term,
        min_principal_amount=product.min_principal_amount,
        max_principal_amount=product.max_principal_amount,
        min_interest=product.min_interest,
        max_interest=product.max_interest,
        min_origination_amount=product.min_origination_amount,
        max_origination_amount=product.max_origination_amount,
    )


@app.post('/product', summary='Create new product')
async def set_product(
        product_to_post: ProductCreateDto,
        session: AsyncSession = Depends(get_session)
):
    """
    If product is not available, then create new product.
    :param product_to_post: product to create
    :param session: The connection session with DB
    :return: If product is not available, then return 200, otherwise raise error 409
    """
    product: ProductDao = (await Repository.get(ProductDao, session,
                                                ['code'], [product_to_post.code])).one_or_none()
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
        raise HTTPException(status_code=409, detail=f'Неверные данные, {ex}!')

    await Repository.create(ProductDao, session, product_n)
    return Response(
        media_type='text/plain',
        content='Успешно добавлен!'
    )


@app.delete('/product/{code}', summary='Delete product')
async def deleted_product(code: str, session: AsyncSession = Depends(get_session)):
    """
    Delete product by product code.
    :param code: code of product
    :param session: The connection session with DB
    :return: response 204
    """
    product: ProductDao = (await Repository.get(ProductDao, session,
                                                ['code'], [code])).one_or_none()
    if product:
        await Repository.delete(ProductDao, session, code)
    return Response(
        status_code=204,
        media_type='text/plain',
        content='Продукт с указанным кодом был успешно удален!'
    )


@app.post('/agreement', summary='Create new agreement')
async def set_agreement(
        agreement_to_post: AgreementCreateDto,
        session: AsyncSession = Depends(get_session)
):
    """
    Create new agreement of person.
    :param agreement_to_post: agreement data
    :param session: The connection session with DB
    :return: Agreement id, otherwise 400
    """

    product: ProductDao = (await Repository.get(ProductDao, session,
                                                ['code'], [agreement_to_post.product_code])).one_or_none()
    if product is None:
        raise HTTPException(status_code=400, detail="Продукт с таким кодом не существует")

    person: PersonDao = (
        await Repository.get(PersonDao, session,
                             ['first_nm', 'last_nm', 'middle_nm', 'birth_dt', 'passport_no', 'email'],
                             [agreement_to_post.first_name, agreement_to_post.second_name, agreement_to_post.third_name,
                              datetime.strptime(agreement_to_post.birthday, '%d.%m.%Y'), agreement_to_post.passport_number,
                              agreement_to_post.email])).one_or_none()
    if person:
        person_n = person
    else:
        person_n = PersonDao(
            first_nm=agreement_to_post.first_name,
            last_nm=agreement_to_post.second_name,
            middle_nm=agreement_to_post.third_name,
            birth_dt=datetime.strptime(agreement_to_post.birthday, '%d.%m.%Y'),
            passport_no=agreement_to_post.passport_number,
            email=agreement_to_post.email,
            mobile_phone_no=agreement_to_post.phone,
            monthly_income_amt=int(agreement_to_post.salary)
        )
        await Repository.create(PersonDao, session, person_n)

    origination_amt = random.random() * (float(product.max_origination_amount) - float(product.min_origination_amount))
    origination_amt += float(product.min_origination_amount)

    agreement_n = AgreementDao(
        product_code=agreement_to_post.product_code,
        person_id=person_n.person_id,
        load_term=agreement_to_post.term,
        principal_amount=agreement_to_post.disbursement_amount + origination_amt,
        interest=agreement_to_post.interest,
        origination_amount=origination_amt,
        agreement_dttm=datetime.now(),
        status="NEW"
    )

    if not check_valid_agreement_condition(product=product, agreement=agreement_n):
        raise HTTPException(status_code=400, detail="Данные договора не соответствуют продукту")

    await Repository.create(AgreementDao, session, agreement_n)
    return agreement_n.agreement_id

# if __name__ == "__main__":
#     uvicorn.run("main:app", port=80, log_level="info")
