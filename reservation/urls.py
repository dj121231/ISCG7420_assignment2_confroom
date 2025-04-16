from django.urls import path, reverse
from .views import RoomListView, RoomDetailView, ReservationCreateView, ReservationListView, home

app_name = 'reservation'

urlpatterns = [
    # URL pattern for the home page
    path('', home, name='home'),
    # URL pattern for listing all active rooms
    path('rooms/', RoomListView.as_view(), name='room_list'),
    # URL pattern for viewing a specific room's details
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room_detail'),
    # URL pattern for creating a new reservation for a specific room
    path('rooms/<int:pk>/reserve/', ReservationCreateView.as_view(), name='reservation_create'),
    # URL pattern for viewing reservations of a specific room
    path('rooms/<int:pk>/reservations/', ReservationListView.as_view(), name='reservation_list'),
] 