import asyncio
import unittest

from business_logic.nearest_neighbor_service import optimize_route
from data_access.database.models import Point

class TestOptimizeRoute(unittest.TestCase):
    
    def setUp(self):
        self.points = [
            Point(lat=0, lng=0),
            Point(lat=1, lng=1),
            Point(lat=2, lng=2),
            Point(lat=3, lng=3),
            Point(lat=4, lng=4),
        ]
    
    def test_optimize_route(self):
        optimized_route = asyncio.run(optimize_route(self.points))

        self.assertEqual(len(optimized_route), len(self.points))

        self.assertEqual(len(set(optimized_route)), len(optimized_route))

        for point in self.points:
            self.assertIn(point, optimized_route)

        self.assertEqual(optimized_route[0], optimized_route[-1])
