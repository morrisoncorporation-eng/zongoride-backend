from django.core.management.base import BaseCommand
from fleet.models import Scooter
import random
import string
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Populates the database with scooter data'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='The number of scooters to create')

    def handle(self, *args, **options):
        count = options['count']
        for i in range(count):
            scooter = Scooter.objects.create(
                latitude=random.uniform(34.0, 36.0),
                longitude=random.uniform(-118.0, -120.0),
                serial_number=''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
                battery_level=random.randint(0, 100),
                model_name=random.choice(['Segway Ninebot ES4', 'Xiaomi Mi M365', 'Bird Zero']),
                firmware_version=f'{random.randint(1, 5)}.{random.randint(0, 9)}.{random.randint(0, 9)}',
                last_maintenance_date=date.today() - timedelta(days=random.randint(0, 365)),
                mileage=random.uniform(0, 1000),
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created scooter {scooter.id}'))
