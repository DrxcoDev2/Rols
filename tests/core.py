# tests/test_core.py
import unittest
from backend.core import Router

class TestRouter(unittest.TestCase):
    def test_add_route(self):
        router = Router()
        router.add("/home", lambda req: "hello")
        self.assertIn("/home", router.routes)
        self.assertTrue(callable(router.routes["/home"]))
