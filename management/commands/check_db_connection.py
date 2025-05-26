from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError

class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            db_conn = connections['default']
            db_conn.cursor()
            self.stdout.write(self.style.SUCCESS('Database connection successful'))
            return True
        except OperationalError:
            self.stdout.write(self.style.ERROR('Database connection failed'))
            return False
        