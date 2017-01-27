import sys

from django.apps import apps
from django.conf import settings
from django.core.management.base import CommandError
from django.core.management.commands.makemigrations import Command as MakeMigrationCommand
from django.db import connections, DEFAULT_DB_ALIAS, router
from django.db.migrations import Migration
from django.db.migrations.autodetector import MigrationAutodetector
from django.db.migrations.loader import MigrationLoader
from django.db.migrations import operations, SeparateDatabaseAndState
from django.db.migrations.questioner import (
    InteractiveMigrationQuestioner, MigrationQuestioner,
    NonInteractiveMigrationQuestioner,
)
from django.db.migrations.state import ProjectState
from django.db.migrations.writer import MigrationWriter


class Command(MakeMigrationCommand):
    help = "Creates migrations for moving model from base_app to target_app"

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
        parser.add_argument(
            '--noinput', '--no-input',
            action='store_false', dest='interactive', default=True,
            help='Tells Django to NOT prompt the user for input of any kind.',
        )
        parser.add_argument(
            '--dry-run', action='store_true', dest='dry_run', default=False,
            help="Just show what migrations would be made; don't actually write them.",
        )

    def handle(self, *args, **options):
        self.model = options['model']
        self.base_app = options['base_app']
        self.target_app = options['target_app']
        self.app_labels = (self.base_app, self.target_app)
        self.interactive = options['interactive']
        self.verbosity = options['verbosity']
        self.dry_run = options['dry_run']

        for app_label in self.app_labels:
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

        if conflicts:
            name_str = "; ".join(
                "%s in %s" % (", ".join(names), app)
                for app, names in conflicts.items()
            )
            raise CommandError(
                "Conflicting migrations detected; multiple leaf nodes in the "
                "migration graph: (%s).\nTo fix them run "
                "'python manage.py makemigrations --merge'" % name_str
            )

        self.questioner = InteractiveMigrationQuestioner if self.interactive else NonInteractiveMigrationQuestioner

        # 1
        # first migration for base_app, manually AlterModelTable + SeperateStateAndDb

        loader = MigrationLoader(None, ignore_no_migrations=True)
        autodetector = MigrationAutodetector(
            loader.project_state(),
            ProjectState.from_apps(apps),
            self.questioner(specified_apps=(self.base_app, )),
        )
        autodetector.generated_operations = {}
        autodetector.add_operation(
            self.base_app,
            SeparateDatabaseAndState(
                database_operations=operations.AlterModelTable(
                    name=self.model,
                    table=self.target_app + '_' + self.model
                )
            )
        )
        autodetector._sort_migrations()
        autodetector._build_migration_list()

        changes = autodetector.arrange_for_graph(
            changes=autodetector.migrations,
            graph=loader.graph,
        )
        first_base_app_migration_name = changes[self.base_app][0].name
        self.write_migration_files(changes)

        # 2
        # migrations for target_app, Create model in second App

        loader = MigrationLoader(None, ignore_no_migrations=True)
        autodetector = MigrationAutodetector(
            loader.project_state(),
            ProjectState.from_apps(apps),
            self.questioner(specified_apps=(self.target_app, )),
        )
        autodetector.generated_operations = {}

        # parameters below must be fed to generate_created_models()
        # they imitate the logic of operations keeping the logic

        autodetector.old_apps = autodetector.from_state.concrete_apps
        autodetector.new_apps = autodetector.to_state.apps
        autodetector.old_model_keys = []
        autodetector.old_proxy_keys = []
        autodetector.old_unmanaged_keys = []
        autodetector.new_model_keys = [(self.target_app, self.model)]
        autodetector.new_proxy_keys = []
        autodetector.new_unmanaged_keys = []

        autodetector.generate_created_models()

        autodetector._sort_migrations()
        autodetector._build_migration_list()
        import pdb
        pdb.set_trace()
        created_operations = autodetector.migrations
        assert len(created_operations) == 1, "Step two went wrong."
        create_operation = created_operations[self.target_app][0].operations
        assert len(create_operation) == 1, "Step two went wrong."

        # wrap the migration in state_operation
        autodetector.migrations[self.target_app][0].operations \
            = [SeparateDatabaseAndState(state_operations=create_operation)]

        # add the depencency to the migration
        autodetector.migrations[self.target_app][0].dependencies.append((self.base_app, first_base_app_migration_name))

        changes = autodetector.arrange_for_graph(
            changes=autodetector.migrations,
            graph=loader.graph,
        )

        first_target_app_migration_name = changes[self.target_app][0].name

        self.write_migration_files(changes)

        # 3
        # Third step, resolving all Relational Fields in other apps

        all_apps = set(config.label for config in apps.get_app_configs())
        loader = MigrationLoader(None, ignore_no_migrations=True)
        autodetector = MigrationAutodetector(
            loader.project_state(),
            ProjectState.from_apps(apps),
            self.questioner(specified_apps=all_apps),
        )

        autodetector._prepare_field_lists()
        autodetector.generate_altered_fields()

        for app, migrations in autodetector.migrations.items():
            for migration in migrations:
                migration.dependencies.append(
                    (self.base_app, first_base_app_migration_name),
                    (self.target_app, first_target_app_migration_name)
                )

        changes = autodetector.changes(
            graph=loader.graph,
            trim_to_apps=all_apps,
            convert_apps=all_apps,
        )
        self.write_migration_files(changes)

        # 4
        # Fourth step, delete model from state in base_app

        loader = MigrationLoader(None, ignore_no_migrations=True)
        autodetector = MigrationAutodetector(
            loader.project_state(),
            ProjectState.from_apps(apps),
            self.questioner(specified_apps=(self.base_app,)),
        )
        autodetector.generated_operations = {}
        autodetector.add_operation(
            self.base_app,
            SeparateDatabaseAndState(
                database_operations=operations.DeleteModel(
                    name=self.model,
                )
            )
        )
        autodetector._sort_migrations()
        autodetector._build_migration_list()

        changes = autodetector.arrange_for_graph(
            changes=autodetector.migrations,
            graph=loader.graph,
        )
        self.write_migration_files(changes)
