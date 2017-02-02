from django.apps import apps
from django.test import TestCase
from unittest.mock import patch

from migration_helper.management.commands import move_model


class TestMoveModelApp(TestCase):
    """
    Here we test moving model between <base_app> and <target_app>
    """
    def setUp(self):
        pass
