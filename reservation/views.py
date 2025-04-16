from django.shortcuts import render
from django.views.generic import ListView
from .models import Room

# Create your views here.

class RoomListView(ListView):
    """
    A view that displays a list of all active meeting rooms.
    
    Attributes:
        model: The Room model to be used for the list view
        template_name: The template to render the list
        context_object_name: The name of the object list in the template
        queryset: Custom queryset to filter active rooms
    """
    model = Room
    template_name = 'reservation/rooms.html'
    context_object_name = 'rooms'
    
    def get_queryset(self):
        """
        Returns a queryset of active rooms, ordered by name.
        
        Returns:
            QuerySet: A filtered queryset containing only active rooms
        """
        return Room.objects.filter(is_active=True).order_by('name')
