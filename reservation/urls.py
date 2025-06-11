from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, ReservationViewSet, UserViewSet

router = DefaultRouter()
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'reservations', ReservationViewSet, basename='reservation')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('api/', include(router.urls)),
] 