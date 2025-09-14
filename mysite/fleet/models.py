
from django.contrib.gis.db import models
from django.contrib.auth.models import User
from django.contrib.gis.geos import Point

class Scooter(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('maintenance', 'Maintenance'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    location = models.PointField(null=True, blank=True)
    serial_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    battery_level = models.IntegerField(default=100)
    model_name = models.CharField(max_length=100, blank=True)
    firmware_version = models.CharField(max_length=50, blank=True)
    last_maintenance_date = models.DateField(null=True, blank=True)
    mileage = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def save(self, *args, **kwargs):
        if self.latitude and self.longitude:
            self.location = Point(float(self.longitude), float(self.latitude), srid=4326)
        super(Scooter, self).save(*args, **kwargs)

    def __str__(self):
        return f"Scooter {self.id} - {self.status}"

class Service(models.Model):
    scooter = models.ForeignKey(Scooter, on_delete=models.CASCADE)
    service_date = models.DateField()
    description = models.TextField()

    def __str__(self):
        return f"Service for Scooter {self.scooter.id} on {self.service_date}"

class Bike(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('maintenance', 'Maintenance'),
    )
    BIKE_TYPE_CHOICES = (
        ('road', 'Road'),
        ('mountain', 'Mountain'),
        ('electric', 'Electric'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    bike_type = models.CharField(max_length=20, choices=BIKE_TYPE_CHOICES, default='electric')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    location = models.PointField(null=True, blank=True)
    serial_number = models.CharField(max_length=100, unique=True, null=True, blank=True)
    battery_level = models.IntegerField(default=100, null=True, blank=True)
    model_name = models.CharField(max_length=100, blank=True)
    last_maintenance_date = models.DateField(null=True, blank=True)
    mileage = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def save(self, *args, **kwargs):
        if self.latitude and self.longitude:
            self.location = Point(float(self.longitude), float(self.latitude), srid=4326)
        super(Bike, self).save(*args, **kwargs)

    def __str__(self):
        return f"Bike {self.id} - {self.status}"

class RideHistory(models.Model):
    rider = models.ForeignKey(User, on_delete=models.CASCADE)
    scooter = models.ForeignKey(Scooter, on_delete=models.CASCADE)
    start_time = models.DateTimeField(auto_now_add=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DurationField(null=True, blank=True)

    def __str__(self):
        return f"Ride by {self.rider.username} on {self.scooter.id}"
