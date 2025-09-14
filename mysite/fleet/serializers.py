
from rest_framework import serializers
from .models import Scooter, Bike, RideHistory

class ScooterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scooter
        fields = ('id', 'status', 'latitude', 'longitude', 'serial_number', 'battery_level', 'model_name', 'firmware_version', 'last_maintenance_date', 'mileage')

class BikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bike
        fields = ('id', 'status', 'bike_type', 'latitude', 'longitude', 'serial_number', 'battery_level', 'model_name', 'last_maintenance_date', 'mileage')

class RideHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RideHistory
        fields = ('id', 'rider', 'scooter', 'start_time', 'end_time', 'duration')
