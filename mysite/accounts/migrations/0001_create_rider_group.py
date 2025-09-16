
from django.db import migrations

def create_rider_group(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    
    # Get the content type for the Scooter model
    # This ensures that we can create the permissions if they don't exist
    scooter_content_type = ContentType.objects.get(
        app_label='fleet',
        model='scooter'
    )

    # Use get_or_create to be safe. It will find the permission if it exists,
    # or create it if it doesn't.
    view_scooter, created = Permission.objects.get_or_create(
        codename='view_scooter',
        content_type=scooter_content_type,
        defaults={'name': 'Can view scooter'}
    )
    change_scooter, created = Permission.objects.get_or_create(
        codename='change_scooter',
        content_type=scooter_content_type,
        defaults={'name': 'Can change scooter'}
    )

    rider_group, created = Group.objects.get_or_create(name='Rider')

    # Add permissions to the group
    rider_group.permissions.add(view_scooter, change_scooter)

class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('fleet', '0003_bike_location_scooter_location'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.RunPython(create_rider_group),
    ]
