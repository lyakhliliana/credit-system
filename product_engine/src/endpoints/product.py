from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from common.generic_repository import GenericRepository
from product_engine.src.models.dao import ProductDao
from product_engine.src.models.dto import ProductDto, ProductCreateDto
from product_engine.src.models.session_maker import get_session

product_router = APIRouter(prefix="/product")


@product_router.get(
    '',
    response_model=list[ProductDto],
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


@product_router.get(
    '/{code}',
    response_model=ProductDto,
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


@product_router.post('', summary='Create new product')
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


@product_router.delete('/{code}', summary='Delete product')
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
