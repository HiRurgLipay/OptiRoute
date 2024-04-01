from typing import List
import math
from tqdm import tqdm

from data_access.database.models import Point


async def calculate_distance(point1: Point, point2: Point) -> float:
    """
    Вычисляет расстояние между двумя точками с использованием евклидова расстояния.
    """
    return math.sqrt((point1.lat - point2.lat)**2 + (point1.lng - point2.lng)**2)


async def find_closest_point(current_point: Point, remaining_points: List[Point]) -> Point:
    """
    Находит ближайшую точку к текущей точке.
    """
    closest_point = None
    min_distance = float('inf')

    for point in remaining_points:
        distance = await calculate_distance(current_point, point)
        if distance < min_distance:
            min_distance = distance
            closest_point = point

    return closest_point


async def optimize_route(points: List[Point]) -> List[Point]:
    """
    Оптимизирует маршрут с использованием алгоритма ближайшего соседа.
    """
    optimized_route = []
    remaining_points = points.copy()

    current_point = remaining_points.pop(0)
    optimized_route.append(current_point)

    with tqdm(total=len(points), desc="Оптимизация маршрута") as pbar:
        while remaining_points:
            closest_point = await find_closest_point(current_point, remaining_points)
            optimized_route.append(closest_point)
            remaining_points.remove(closest_point)
            current_point = closest_point
            pbar.update(1)

    return optimized_route
