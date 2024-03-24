from typing import Sequence, TypeVar, Generic
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, ColumnElement

from common.base_orm_model import BaseOrmModel

T = TypeVar("T", bound=BaseOrmModel)


class GenericRepository(Generic[T]):
    def __init__(self, session: AsyncSession, entity: T):
        self.__entity: T = entity
        self.__session: AsyncSession = session

    async def get_all_by_params_and(self, columns: list, values: list) -> Sequence[T]:
        f: ColumnElement[bool] = self.__entity.__table__.columns[columns[0]] == values[0]
        for i in range(1, len(values)):
            f &= self.__entity.__table__.columns[columns[i]] == values[i]
        return (await self.__session.execute(select(self.__entity).where(f))).unique().scalars().all()

    async def get_all_by_params_or(self, columns: list, values: list) -> Sequence[T]:
        f = self.__entity.__table__.columns[columns[0]] == values[0]
        for i in range(1, len(values)):
            f |= self.__entity.__table__.columns[columns[i]] == values[i]
        return (await self.__session.execute(select(self.__entity).where(f))).unique().scalars().all()

    async def get_one_by_params(self, columns: list, values: list) -> T:
        f = self.__entity.__table__.columns[columns[0]] == values[0]
        for i in range(1, len(values)):
            f &= self.__entity.__table__.columns[columns[i]] == values[i]
        return (await self.__session.execute(select(self.__entity).where(f))).unique().scalars().one_or_none()

    async def get_all(self) -> Sequence[T]:
        return (await self.__session.execute(select(self.__entity))).unique().scalars().all()

    async def save(self, value: T):
        self.__session.add(value)
        await self.__session.commit()
        await self.__session.refresh(value)

    async def delete(self, code):
        await self.__session.execute(delete(self.__entity).where(self.__entity.code == code))
        await self.__session.commit()

    async def update_property(self, columns_find: list, values_find: list, column_update: str, value_update: str):
        f = self.__entity.__table__.columns[columns_find[0]] == values_find[0]
        for i in range(1, len(values_find)):
            f &= self.__entity.__table__.columns[columns_find[i]] == values_find[i]
        await self.__session.execute(update(self.__entity).where(f).values(**{column_update: value_update}))
        await self.__session.commit()
