
from django.db import migrations

def create_rider_group(apps, schema_editor):
    # Get historical models from the app registry
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')
    Scooter = apps.get_model('fleet', 'Scooter')

    # Use the recommended, robust way to get the content type for a model
    # during a migration.
    scooter_content_type = ContentType.objects.get_for_model(Scooter)

    # Use get_or_create to safely find or create the permissions
    view_scooter, _ = Permission.objects.get_or_create(
        codename='view_scooter',
        content_type=scooter_content_type,
        defaults={'name': 'Can view scooter'}
    )
    change_scooter, _ = Permission.objects.get_or_create(
        codename='change_scooter',
        content_type=scooter_content_type,
        defaults={'name': 'Can change scooter'}
    )

    # Create the 'Rider' group
    rider_group, _ = Group.objects.get_or_create(name='Rider')

    # Add the permissions to the group
    rider_group.permissions.add(view_scooter, change_scooter)

class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('fleet', '0003_bike_location_scooter_location'),
        # This dependency is important to ensure ContentType model is available
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.RunPython(create_rider_group),
    ]
