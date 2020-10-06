import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to pause exceute until db ready"""

    def handle(self, *args, **options):
        self.stdout.write('waiting for db...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write("DB unavailable, waiting for 1 s")
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('DB is available'))
