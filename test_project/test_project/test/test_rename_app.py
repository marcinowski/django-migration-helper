from django.apps import apps
from django.test import TestCase

from base_app.management import FillDatabase


class TestRenameApp(TestCase):
    """
    Here we are going to rename app from rename_app
    """
    def setUp(self):
        FillDatabase.run()
        state_before_renaming = apps.get_app_configs()

    def test_if_rename_app_exists(self):
        self.assertRaises(apps.get_app_config('rename_app_test'))
        self.assertIsNotNone(apps.get_app_config('rename_app'))
