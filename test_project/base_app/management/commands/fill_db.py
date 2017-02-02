from django.core.management.base import BaseCommand

from base_app.services import FillDatabase


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            '--noclean', '--no-clean',
            action='store_false', dest='clean_db', default=True,
            help='Don\' clean db data while running this command.',
        )

    def handle(self, *args, **options):
        FillDatabase.run(clean_db=options['clean_db'])
