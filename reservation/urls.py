from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomViewSet, ReservationViewSet, UserViewSet, get_reserved_times, get_available_dates, CurrentUserView, RegisterView, CustomTokenObtainPairView

router = DefaultRouter()
router.register(r'rooms', RoomViewSet, basename='room')
router.register(r'reservations', ReservationViewSet, basename='reservation')
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('reserved-times/', get_reserved_times.as_view(), name='get_reserved_times'),
    path('available-dates/', get_available_dates.as_view(), name='get_available_dates'),
    path('me/', CurrentUserView.as_view(), name='current-user'),
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
] 