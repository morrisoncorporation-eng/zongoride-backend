from django.contrib import admin
from .models import Scooter, Bike

@admin.register(Scooter)
class ScooterAdmin(admin.ModelAdmin):
    list_display = ('id', 'serial_number', 'status', 'model_name', 'battery_level', 'mileage', 'last_maintenance_date')
    list_filter = ('status', 'model_name')
    search_fields = ('serial_number', 'model_name')

@admin.register(Bike)
class BikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'serial_number', 'status', 'bike_type', 'model_name', 'battery_level', 'mileage', 'last_maintenance_date')
    list_filter = ('status', 'bike_type', 'model_name')
    search_fields = ('serial_number', 'model_name')
