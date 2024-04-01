from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data_access.database.models import Route


async def get_route(db: AsyncSession, route_id: int) -> Route:
    """
    Получение маршрута по его идентификатору из базы данных.
    """
    result = await db.execute(select(Route).filter(Route.id == route_id))
    return result.scalars().first()


async def create_route(db: AsyncSession, route: Route) -> Route:
    """
    Создание нового маршрута в базе данных.
    """
    db.add(route)
    await db.commit()
    await db.refresh(route)
    return route
