from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from data_access.database.models import Point


async def get_optimized_points(db: AsyncSession, route_id: int) -> List[dict]:
    """
    Получение оптимизированных точек маршрута по его идентификатору из базы данных.
    """
    statement = select(Point).filter(Point.route_id == route_id)
    result = await db.execute(statement)
    
    # Преобразуем объекты Point в словари с ключами "lat" и "lng"
    formatted_points = [{"lat": point.lat, "lng": point.lng} for point in result.scalars().all()]
    
    return formatted_points
