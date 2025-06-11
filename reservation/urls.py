from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, ReservationViewSet, UserViewSet, get_reserved_times, get_available_dates

router = DefaultRouter()
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'reservations', ReservationViewSet, basename='reservation')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/reserved-times/', get_reserved_times.as_view(), name='get_reserved_times'),
    path('api/available-dates/', get_available_dates.as_view(), name='get_available_dates'),
] 