from pprint import pformat
from django.core.management.base import BaseCommand, CommandError
from biodata.api.factory import COUNTS, StudyFactory
from biodata.api.models import Study


class Command(BaseCommand):
    help = 'Loads the database with fake biological data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--study_count',
            type=int,
            default=COUNTS[Study],
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

        studies = StudyFactory.create_batch(options['study_count'])
        counts = {
            typ.__name__: typ.objects.count()
            for typ in COUNTS
        }

        self.stdout.write(self.style.SUCCESS(
            f'Successfully loaded fake data:\n{pformat(counts)}'
        ))
