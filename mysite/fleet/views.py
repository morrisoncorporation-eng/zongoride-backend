
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Scooter, Bike, RideHistory
from .serializers import ScooterSerializer, BikeSerializer, RideHistorySerializer
from django.utils import timezone
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from drf_spectacular.utils import extend_schema, OpenApiExample
from django.shortcuts import render

@extend_schema(
    description="Operations related to the management of the scooter fleet."
)
class ScooterListCreateView(generics.ListCreateAPIView):
    """
    API endpoint that allows for the listing and creation of scooters.
    """
    queryset = Scooter.objects.all()
    serializer_class = ScooterSerializer
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="List all scooters",
        description="Retrieve a list of all scooters in the fleet, including their real-time status and location.",
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @extend_schema(
        summary="Add a new scooter to the fleet",
        description="Create a new scooter record. This is typically used when a new scooter is commissioned into the fleet.",
        examples=[
            OpenApiExample(
                'Example Request',
                summary='A sample request to add a new scooter',
                description='Provide the scooter model, current status, and its initial GPS location.',
                value={
                    "model": "Zongo X1",
                    "status": "available",
                    "location": {
                        "type": "Point",
                        "coordinates": [-73.985, 40.748]
                    }
                },
                request_only=True
            )
        ]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ScooterRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Scooter.objects.all()
    serializer_class = ScooterSerializer
    permission_classes = [IsAuthenticated]

class LockScooterView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        scooter = Scooter.objects.get(pk=pk)
        scooter.status = 'available'
        scooter.save()

        ride = RideHistory.objects.filter(scooter=scooter, rider=request.user, end_time__isnull=True).last()
        if ride:
            ride.end_time = timezone.now()
            ride.duration = ride.end_time - ride.start_time
            ride.save()

        serializer = ScooterSerializer(scooter)
        return Response(serializer.data)

class UnlockScooterView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        scooter = Scooter.objects.get(pk=pk)
        scooter.status = 'in_use'
        scooter.save()

        RideHistory.objects.create(scooter=scooter, rider=request.user)

        serializer = ScooterSerializer(scooter)
        return Response(serializer.data)

class BikeListCreateView(generics.ListCreateAPIView):
    queryset = Bike.objects.all()
    serializer_class = BikeSerializer
    permission_classes = [IsAuthenticated]

class BikeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bike.objects.all()
    serializer_class = BikeSerializer
    permission_classes = [IsAuthenticated]

class RideHistoryListView(generics.ListAPIView):
    serializer_class = RideHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return RideHistory.objects.filter(rider=self.request.user)

class NearbyScootersView(generics.ListAPIView):
    serializer_class = ScooterSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        latitude = self.request.query_params.get('latitude')
        longitude = self.request.query_params.get('longitude')

        if not latitude or not longitude:
            return Scooter.objects.none()

        user_location = Point(float(longitude), float(latitude), srid=4326)
        return Scooter.objects.filter(status='available').annotate(distance=Distance('location', user_location)).order_by('distance')

class ScooterGeoJSONListView(APIView):
    """
    API endpoint that provides a GeoJSON representation of all scooters.
    This is suitable for use with mapping libraries like Leaflet.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        scooters = Scooter.objects.all()
        features = []
        for scooter in scooters:
            if scooter.location:
                feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": [scooter.location.x, scooter.location.y]
                    },
                    "properties": {
                        "id": scooter.id,
                        "status": scooter.status,
                        "battery_level": scooter.battery_level,
                    }
                }
                features.append(feature)
        
        feature_collection = {
            "type": "FeatureCollection",
            "features": features
        }
        
        return Response(feature_collection)

def map_view(request):
    """
    This view renders the live map page for the scooter fleet.
    """
    return render(request, 'fleet/map.html')
