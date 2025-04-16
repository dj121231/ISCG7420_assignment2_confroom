from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .models import Room, Reservation

# Create your views here.

def home(request):
    """
    A simple view that displays a welcome message and a link to the rooms page.
    
    Args:
        request: The HTTP request object
        
    Returns:
        HttpResponse: A response containing the welcome message and link
    """
    welcome_message = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Conference Room Booking System</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                line-height: 1.6;
            }
            .welcome {
                text-align: center;
                margin-top: 50px;
            }
            .link {
                display: inline-block;
                margin-top: 20px;
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                text-decoration: none;
                border-radius: 5px;
            }
            .link:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <div class="welcome">
            <h1>Welcome to the Conference Room Booking System</h1>
            <p>Manage your meeting room reservations efficiently and easily.</p>
            <a href="/rooms/" class="link">View Available Rooms</a>
        </div>
    </body>
    </html>
    """
    return HttpResponse(welcome_message)

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

class RoomDetailView(DetailView):
    """
    A view that displays detailed information about a specific meeting room.
    
    Attributes:
        model: The Room model to be used for the detail view
        template_name: The template to render the detail view
        context_object_name: The name of the object in the template
        queryset: Custom queryset to filter active rooms
    """
    model = Room
    template_name = 'reservation/room_detail.html'
    context_object_name = 'room'
    
    def get_queryset(self):
        """
        Returns a queryset of active rooms.
        
        Returns:
            QuerySet: A filtered queryset containing only active rooms
        """
        return Room.objects.filter(is_active=True)

class ReservationListView(ListView):
    """
    A view that displays a list of reservations for a specific room.
    
    Attributes:
        model: The Reservation model to be used
        template_name: The template to render the list
        context_object_name: The name of the object list in the template
    """
    model = Reservation
    template_name = 'reservation/reservation_list.html'
    context_object_name = 'reservations'
    
    def get_queryset(self):
        """
        Returns a queryset of reservations for the specified room,
        ordered by date and start time.
        
        Returns:
            QuerySet: A filtered queryset containing reservations for the room
        """
        room = get_object_or_404(Room, pk=self.kwargs['pk'])
        return Reservation.objects.filter(room=room).order_by('date', 'start_time')
    
    def get_context_data(self, **kwargs):
        """
        Adds the room object to the template context.
        
        Args:
            **kwargs: Additional context data
            
        Returns:
            dict: The context dictionary with the room object added
        """
        context = super().get_context_data(**kwargs)
        context['room'] = get_object_or_404(Room, pk=self.kwargs['pk'])
        return context

class ReservationCreateView(LoginRequiredMixin, CreateView):
    """
    A view that handles the creation of new room reservations.
    
    Attributes:
        model: The Reservation model to be used
        template_name: The template to render the form
        fields: The fields to include in the form
    """
    model = Reservation
    template_name = 'reservation/reservation_form.html'
    fields = ['title', 'description', 'date', 'start_time', 'end_time']
    
    def get_room(self):
        """
        Returns the room object based on the URL's pk parameter.
        
        Returns:
            Room: The room object for the reservation
        """
        return get_object_or_404(Room, pk=self.kwargs['pk'])
    
    def get_context_data(self, **kwargs):
        """
        Adds the room object to the template context.
        
        Args:
            **kwargs: Additional context data
            
        Returns:
            dict: The context dictionary with the room object added
        """
        context = super().get_context_data(**kwargs)
        context['room'] = self.get_room()
        return context
    
    def form_valid(self, form):
        """
        Sets the room and user for the reservation before saving.
        
        Args:
            form: The validated form instance
            
        Returns:
            HttpResponseRedirect: Redirects to the success URL
        """
        form.instance.room = self.get_room()
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        """
        Returns the URL to redirect to after successful form submission.
        
        Returns:
            str: The URL to redirect to
        """
        return reverse('reservation:room_detail', kwargs={'pk': self.kwargs['pk']})
