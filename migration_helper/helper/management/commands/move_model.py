import sys

from django.apps import apps
from django.conf import settings
from django.core.checks import Tags, run_checks
from django.core.management import BaseCommand
from django.db import connections, DEFAULT_DB_ALIAS, router
from django.db.migrations.loader import MigrationLoader
from django.core.management.commands.makemigrations import Command as MakeMigrationCommand
from django.core.management.commands.migrate import Command as MigrateCommand
from django.core.management.commands.showmigrations import Command as ShowMigrationsCommand


class Command(BaseCommand):
    help = "Creates migrations for moving model from app_1 to app_2"

    def add_arguments(self, parser):
        parser.add_argument(
            'model',
            help='Name of a model to be transferred',
        )
        parser.add_argument(
            'base_app',
            help='App label from where to move model.',
        )
        parser.add_argument(
            'target_app',
            help='App label to put the model into',
        )
        parser.add_argument(
            '--database', action='store', dest='database',
            default=DEFAULT_DB_ALIAS,
            help='Nominates a database to synchronize. Defaults to the "default" database.',
        )

    def _run_checks(self, **kwargs):
        issues = run_checks(tags=[Tags.database])
        issues.extend(super(Command, self)._run_checks(**kwargs))
        return issues

    def handle(self, *args, **options):
        self.model = options['model']
        self.base_app = options['base_app']
        self.target_app = options['target_app']

        for app_label in (self.base_app, self.target_app):
            try:
                apps.get_app_config(app_label)
            except LookupError:
                self.stderr.write("App '%s' could not be found. Is it in INSTALLED_APPS?" % app_label)
                sys.exit(2)
        db = options['database']
        connection = connections[db]
        connection.prepare_database()

        # Load the current graph state. Pass in None for the connection so
        # the loader doesn't try to resolve replaced migrations from DB.
        loader = MigrationLoader(None, ignore_no_migrations=True)

        # Raise an error if any migrations are applied before their dependencies.
        consistency_check_labels = set(config.label for config in apps.get_app_configs())
        # Non-default databases are only checked if database routers used.
        aliases_to_check = connections if settings.DATABASE_ROUTERS else [DEFAULT_DB_ALIAS]
        for alias in sorted(aliases_to_check):
            connection = connections[alias]
            if (connection.settings_dict['ENGINE'] != 'django.db.backends.dummy' and any(
                    # At least one model must be migrated to the database.
                    router.allow_migrate(connection.alias, app_label, model_name=model._meta.object_name)
                    for app_label in consistency_check_labels
                    for model in apps.get_app_config(app_label).get_models()
            )):
                loader.check_consistent_history(connection)

        conflicts = loader.detect_conflicts()