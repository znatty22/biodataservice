from django.core.management.base import BaseCommand, CommandError
from biodata.api.factory import COUNTS, StudyFactory
from biodata.api.models import Study


DEFAULT_STUDY_COUNT = COUNTS[Study]


class Command(BaseCommand):
    help = 'Loads the database with fake biological data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--study_count',
            type=int,
            default=DEFAULT_STUDY_COUNT,
            help='Delete data before loading',
        )
        parser.add_argument(
            '--delete',
            default=True,
            help='Delete data before loading',
        )

    def handle(self, *args, **options):
        if options['delete']:
            count = Study.objects.count()
            self.stdout.write(self.style.WARNING(
                f'Deleting {count} existing studies ...'
            ))
            Study.objects.all().delete()

        for i in range(options['study_count']):
            s = StudyFactory()
            self.stdout.write(self.style.SUCCESS(
                f'Created study {s}'
            ))

        self.stdout.write(self.style.SUCCESS(
            f'Successfully loaded {DEFAULT_STUDY_COUNT} studies into database')
        )
