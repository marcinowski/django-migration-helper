import sys

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.migrations.recorder import MigrationRecorder


class Command(BaseCommand):
    """
    http://stackoverflow.com/questions/8408046/how-to-change-the-name-of-a-django-app
    """

    help = "Renames <base_app> to <target_app> keeping all the data and taking care of all previous migrations."

    def add_arguments(self, parser):
        parser.add_argument(
            'base_app',
            help='Existing app label to be renamed.',
        )
        parser.add_argument(
            'target_app',
            help='Target label for app.',
        )
        parser.add_argument(
            '--database', action='store', dest='database', default=DEFAULT_DB_ALIAS,
            help='Nominates a database to modify. Defaults to the "default" database.',
        )
        parser.add_argument(
            '--noinput', '--no-input',
            action='store_false', dest='interactive', default=True,
            help='Tells Django to NOT prompt the user for input of any kind.',
        )

    def handle(self, *args, **options):
        self.base_app = options['base_app']
        self.target_app = options['target_app']
        self.database = options['database']

        self.verbosity = options['verbosity']
        self.interactive = options['interactive']

        connection = connections[self.database]

        self.stdout.write(self.style.NOTICE("  Renaming {} to {}.".format(self.base_app, self.target_app))
                          ) if self.verbosity else None
        # [0] Perform some checks about apps_labels, apps state, db state and migrations
        self._verify_input()

        # [1] Edit django_content_type table, alter <base_app> to <target_app> (also in model) ContentType
        self.stdout.write(self.style.NOTICE("  Renaming content types.")) if self.verbosity else None
        for ctype in ContentType.objects.all():
            if ctype.app_label == self.base_app:
                ctype.app_label = self.target_app
                count = ctype.model.count(self.base_app)
                if count:
                    ctype.model = ctype.model[:-len(self.base_app)] + self.target_app
                ctype.save()

        # [2] Rename model tables under <base_app> BaseDatabaseSchemaEditor
        self.stdout.write(self.style.NOTICE("  Renaming database tables.")) if self.verbosity else None
        with connection.schema_editor(atomic=True) as schema_editor:
            for model, state in apps.get_app_config(self.target_app).models.items():
                default_old_name = '_'.join((self.base_app, model))
                if default_old_name == state._meta.db_table:
                    new_name = '_'.join((self.target_app, model))
                    schema_editor.alter_db_table(model, default_old_name, new_name)

        # [3] Edit django_migrations table, MigrationRecorder.Migration
        self.stdout.write(self.style.NOTICE("  Renaming migration tables.")) if self.verbosity else None
        for migration in MigrationRecorder.Migration.objects.all():
            if migration.app == self.base_app:
                migration.app = self.target_app
                migration.save()

        self.stdout.write(self.style.NOTICE("  Done.")) if self.verbosity else None

    def _verify_input(self):
        # check if provided apps exist and been renamed
        try:
            apps.get_app_config(self.target_app)
        except LookupError:
            self.stderr.write(
                "Did you rename the '%s' app physically and resolved all imports and string occurrences?"
                % self.base_app
            )
            sys.exit(2)
        try:
            apps.get_app_config(self.base_app)
        except LookupError:
            pass
        else:
            self.stderr.write(
                "Did you rename the '%s' app physically and resolved all imports and string occurrences?"
                % self.base_app
            )
            sys.exit(2)

    def _show_info(self):
        info = [
            'hehe',
            'jeje',
            'ojoj'
        ]
        if self.verbosity >= 1:
            yield self.stdout.write(
                self.style.NOTICE(info)
            )
