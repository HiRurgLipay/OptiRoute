from data_access.database.database import async_session

from sqlalchemy.ext.asyncio import AsyncSession


async def get_db() -> AsyncSession:
    """
    Функция для получения асинхронного сеанса с базой данных.
    """
    return async_session()
