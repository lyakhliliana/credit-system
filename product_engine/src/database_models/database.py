from sqlalchemy import select, ScalarResult, delete
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+asyncpg://postgres:postgres@postgresql:5432/product_engine"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session


class Repository:
    @staticmethod
    async def get(table: Base, session: AsyncSession, columns: list, values: list) -> ScalarResult:
        f = table.__table__.columns[columns[0]] == values[0]
        for i in range(1, len(values)):
            f &= table.__table__.columns[columns[i]] == values[i]
        return (await session.execute(select(table).where(f))).scalars()

    @staticmethod
    async def get_all(table: Base, session: AsyncSession) -> ScalarResult:
        return (await session.execute(select(table))).scalars()

    @staticmethod
    async def create(table: Base, session: AsyncSession, value: Base):
        session.add(value)
        await session.commit()
        await session.refresh(value)

    @staticmethod
    async def delete(table: Base, session: AsyncSession, code):
        await session.execute(delete(table).where(table.code == code))
        await session.commit()
