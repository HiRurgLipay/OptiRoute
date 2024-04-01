from fastapi import  HTTPException, Query, UploadFile, File
from fastapi.responses import JSONResponse

from business_logic import read_csv, optimize_route
from presentation.router import router
from data_access.db_services import (
    get_optimized_points,
    get_route,
    create_route
)
from data_access.database.models import Route
from data_access.database.session import get_db



@router.post("/routes")
async def upload_file(file: UploadFile = File(..., description="Загрузите CSV файл для обработки")):
    """
    POST запрос для создания нового маршрута.
    Функция считывает CSV-файл из параметра запроса, оптимизирует маршрут,
    создает объект маршрута в базе данных и возвращает оптимизированный маршрут.
    """
    try:
        contents = await file.read()
        points = await read_csv(contents.decode())
        optimized_points = await optimize_route(points)
        route = Route(points=optimized_points)
        db = await get_db()
        created_route = await create_route(db, route)
        route_id = created_route.id
        optimized_points = await get_optimized_points(db, route_id)
        return {
            "id": created_route.id,
            "points": optimized_points
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"message": str(e)})


@router.get("/routes/{id}")
async def get_route_by_id(id: int, page: int = Query(1, ge=1), limit: int = Query(3, ge=1, le=100)):
    """
    GET запрос для получения маршрута по его идентификатору.
    Функция получает маршрут из базы данных по указанному идентификатору,
    оптимизирует точки маршрута с учетом пагинации и возвращает результат.
    """
    try:
        db = await get_db()
        route = await get_route(db, route_id=id)
        if not route:
            raise HTTPException(status_code=404, detail="Route not found")
        
        start_index = (page - 1) * limit
        end_index = start_index + limit
        optimized_points = await get_optimized_points(db, route_id=id)
        paginated_points = optimized_points[start_index:end_index]
        
        return {
            "page": page,
            "id": route.id,
            "points": paginated_points
        }
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
