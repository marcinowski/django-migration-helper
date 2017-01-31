import sys

from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.migrations.recorder import MigrationRecorder


class Command(BaseCommand):
    """

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

        connection = connections[self.database]

        # [0] Perform some checks about apps_labels, apps state, db state and migrations
        self._verify_input()

        # [1] Edit django_content_type table, alter <base_app> to <target_app> (also in model) ContentType
        for ctype in ContentType.objects.all():
            if ctype.app_label == self.base_app:
                ctype.app_label = self.target_app
                count = ctype.model.count(self.base_app)
                if count:
                    ctype.model = ctype.model[:-len(self.base_app)] + self.target_app
                ctype.save()

        # [2] Rename model tables under <base_app> BaseDatabaseSchemaEditor ??

        # [3] Edit django_migrations table, MigrationRecorder.Migration
        for migration in MigrationRecorder.Migration.objects.all():
            if migration.app == self.base_app:
                migration.app = self.target_app
                migration.save()

    def _verify_input(self):
        # check if provided apps exist and been renamed
        try:
            apps.get_app_config(self.target_app)
        except LookupError:
            self.stderr.write("App '%s' could not be found. Is it in INSTALLED_APPS?" % self.target_app)
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
