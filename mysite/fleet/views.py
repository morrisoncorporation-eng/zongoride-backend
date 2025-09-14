
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Scooter, Bike, RideHistory
from .serializers import ScooterSerializer, BikeSerializer, RideHistorySerializer
from django.utils import timezone
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

class ScooterListCreateView(generics.ListCreateAPIView):
    queryset = Scooter.objects.all()
    serializer_class = ScooterSerializer
    permission_classes = [IsAuthenticated]

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
