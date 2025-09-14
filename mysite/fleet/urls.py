
from django.urls import path
from .views import (
    ScooterListCreateView,
    ScooterRetrieveUpdateDestroyView,
    LockScooterView,
    UnlockScooterView,
    BikeListCreateView,
    BikeRetrieveUpdateDestroyView,
    RideHistoryListView,
    NearbyScootersView,
)

urlpatterns = [
    path('scooters/', ScooterListCreateView.as_view(), name='scooter-list-create'),
    path('scooters/nearby/', NearbyScootersView.as_view(), name='scooter-nearby'),
    path('scooters/<int:pk>/', ScooterRetrieveUpdateDestroyView.as_view(), name='scooter-retrieve-update-destroy'),
    path('scooters/<int:pk>/lock/', LockScooterView.as_view(), name='scooter-lock'),
    path('scooters/<int:pk>/unlock/', UnlockScooterView.as_view(), name='scooter-unlock'),
    path('bikes/', BikeListCreateView.as_view(), name='bike-list-create'),
    path('bikes/<int:pk>/', BikeRetrieveUpdateDestroyView.as_view(), name='bike-retrieve-update-destroy'),
    path('ride-history/', RideHistoryListView.as_view(), name='ride-history-list'),
]
