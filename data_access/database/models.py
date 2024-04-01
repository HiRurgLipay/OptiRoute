from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from data_access.database.database import Base

class Point(Base):
    """Модель для точек маршрута."""
    __tablename__ = "points"

    id = Column(Integer, primary_key=True, index=True)
    lat = Column(Float)  # Широта
    lng = Column(Float)  # Долгота
    route_id = Column(Integer, ForeignKey("routes.id"))
    route = relationship("Route", back_populates="points")


class Route(Base):
    """Модель для маршрутов."""
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True, index=True)
    points = relationship("Point", back_populates="route", cascade='all,delete')
