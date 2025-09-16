
from django.db import migrations

def create_rider_group(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    rider_group, created = Group.objects.get_or_create(name='Rider')

    if created:
        # Assuming your scooter app is named 'fleet' and the model is 'Scooter'
        view_scooter = Permission.objects.get(codename='view_scooter')
        change_scooter = Permission.objects.get(codename='change_scooter')

        rider_group.permissions.add(view_scooter, change_scooter)

class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('fleet', '0003_bike_location_scooter_location'),
    ]

    operations = [
        migrations.RunPython(create_rider_group),
    ]
