from django.urls import path, reverse
from .views import (
    RoomListView, RoomDetailView, ReservationCreateView, 
    ReservationListView, ReservationUpdateView, ReservationDeleteView,
    MyReservationListView, ReservationStatusUpdateView, SignupView, home
)

app_name = 'reservation'

urlpatterns = [
    # URL pattern for the home page
    path('', home, name='home'),
    # URL pattern for user registration
    path('signup/', SignupView.as_view(), name='signup'),
    # URL pattern for listing all active rooms
    path('rooms/', RoomListView.as_view(), name='room_list'),
    # URL pattern for viewing a specific room's details
    path('rooms/<int:pk>/', RoomDetailView.as_view(), name='room_detail'),
    # URL pattern for creating a new reservation for a specific room
    path('rooms/<int:pk>/reserve/', ReservationCreateView.as_view(), name='reservation_create'),
    # URL pattern for viewing reservations of a specific room
    path('rooms/<int:pk>/reservations/', ReservationListView.as_view(), name='reservation_list'),
    # URL pattern for editing an existing reservation
    path('reservations/<int:pk>/edit/', ReservationUpdateView.as_view(), name='reservation_edit'),
    # URL pattern for deleting an existing reservation
    path('reservations/<int:pk>/delete/', ReservationDeleteView.as_view(), name='reservation_delete'),
    # URL pattern for viewing user's reservations
    path('my-reservations/', MyReservationListView.as_view(), name='my_reservations'),
    # URL pattern for updating reservation status
    path('reservations/<int:pk>/status/', ReservationStatusUpdateView.as_view(), name='reservation_status_update'),
] 