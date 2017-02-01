from django.apps import apps
from django.test import TestCase
from unittest.mock import patch

from migration_helper.management.commands import rename_app


class TestRenameApp(TestCase):
    """
    Here we are going to rename app from rename_app
    """
    def setUp(self):
        state_before_renaming = apps.get_app_configs()

    def test_if_rename_app_exists(self):
        self.assertRaises(apps.get_app_config('rename_app_test'))
        self.assertIsNotNone(apps.get_app_config('rename_app'))
