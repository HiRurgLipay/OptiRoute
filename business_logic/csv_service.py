from typing import List
import csv
from io import StringIO


from data_access.database.models import Point

async def read_csv(contents: bytes) -> List[Point]:
    """
    Считывает содержимое CSV-файла и возвращает список объектов Point.
    """
    points = []
    file_stream = StringIO(contents)
    reader = csv.DictReader(file_stream)
    total_lines = sum(1 for _ in file_stream)
    file_stream.seek(0)


    for row in reader:
        point = Point(lat=float(row['lat']), lng=float(row['lng']))
        points.append(point)


    return points
