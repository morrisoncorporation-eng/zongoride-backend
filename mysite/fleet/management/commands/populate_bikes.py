from django.core.management.base import BaseCommand
from fleet.models import Bike
import random
import string
from datetime import date, timedelta

class Command(BaseCommand):
    help = 'Populates the database with bike data'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='The number of bikes to create')

    def handle(self, *args, **options):
        count = options['count']
        for i in range(count):
            bike = Bike.objects.create(
                latitude=random.uniform(34.0, 36.0),
                longitude=random.uniform(-118.0, -120.0),
                serial_number=''.join(random.choices(string.ascii_uppercase + string.digits, k=10)),
                battery_level=random.randint(0, 100) if random.choice([True, False]) else None,
                model_name=random.choice(['Schwinn', 'Giant', 'Trek']),
                bike_type=random.choice(['road', 'mountain', 'electric']),
                last_maintenance_date=date.today() - timedelta(days=random.randint(0, 365)),
                mileage=random.uniform(0, 1000),
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created bike {bike.id}'))
