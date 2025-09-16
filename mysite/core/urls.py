from django.urls import path
from .views import rapidoc_view

urlpatterns = [
    path('docs/', rapidoc_view, name='rapidoc'),
]
