import os
from unittest import TestCase

from app.ext import cache
from config import TestingConfig

TEST_DIR = os.path.dirname(os.path.realpath(__file__))

APP_DIR = os.path.dirname(TEST_DIR)


def init_modules_from_config():
    from app.ext import db

    def is_testing():
        return True
    db.is_testing = is_testing
    return db

initdb = init_modules_from_config


class BaseTestCase(TestCase):

    def setUp(self):
        from app.app import create_app
        self.app = create_app(TestingConfig)
        self.db = init_modules_from_config()
        self.app.app_context().push()
        self.fillup()
        cache.clear()

    def fillup(self):
        pass

    def tearDown(self):
        pass
