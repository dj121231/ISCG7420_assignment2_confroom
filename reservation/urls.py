from django.urls import path
from .views import RoomListView

app_name = 'reservation'

urlpatterns = [
    # URL pattern for listing all active rooms
    path('rooms/', RoomListView.as_view(), name='room_list'),
] 