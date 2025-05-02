"""
Views for the conference room booking system.
This module contains all the views for managing rooms and reservations.
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseBadRequest
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic.edit import FormView
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Room, Reservation
import datetime
from django.utils import timezone
from .forms import ReservationForm, AdminReservationForm

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

class RoomCreateView(LoginRequiredMixin, CreateView):
    """
    A view that handles the creation of new meeting rooms.
    Only accessible by staff users.
    
    Attributes:
        model: The Room model to be used
        template_name: The template to render the form
        fields: The fields to include in the form
    """
    model = Room
    template_name = 'reservation/room_form.html'
    fields = ['name', 'capacity', 'location', 'description', 'is_active']
    
    def dispatch(self, request, *args, **kwargs):
        """
        Checks if the user has staff permissions to create a room.
        
        Args:
            request: The HTTP request object
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments
            
        Returns:
            HttpResponse: The response to send to the client
        """
        if not request.user.is_staff:
            return HttpResponseForbidden("You don't have permission to create rooms.")
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        """
        Returns the URL to redirect to after successful form submission.
        
        Returns:
            str: The URL to redirect to
        """
        return reverse('reservation:room_detail', kwargs={'pk': self.object.pk})

class RoomUpdateView(LoginRequiredMixin, UpdateView):
    """
    A view that handles updating existing meeting rooms.
    Only accessible by staff users.
    
    Attributes:
        model: The Room model to be used
        template_name: The template to render the form
        fields: The fields to include in the form
    """
    model = Room
    template_name = 'reservation/room_form.html'
    fields = ['name', 'capacity', 'location', 'description', 'is_active']
    
    def dispatch(self, request, *args, **kwargs):
        """
        Checks if the user has staff permissions to update a room.
        
        Args:
            request: The HTTP request object
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments
            
        Returns:
            HttpResponse: The response to send to the client
        """
        if not request.user.is_staff:
            return HttpResponseForbidden("You don't have permission to update rooms.")
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        """
        Returns the URL to redirect to after successful form submission.
        
        Returns:
            str: The URL to redirect to
        """
        return reverse('reservation:room_detail', kwargs={'pk': self.object.pk})

class RoomDeleteView(LoginRequiredMixin, DeleteView):
    """
    A view that handles deleting existing meeting rooms.
    Only accessible by staff users.
    
    Attributes:
        model: The Room model to be used
        template_name: The template to render the confirmation page
    """
    model = Room
    template_name = 'reservation/room_confirm_delete.html'
    
    def dispatch(self, request, *args, **kwargs):
        """
        Checks if the user has staff permissions to delete a room.
        
        Args:
            request: The HTTP request object
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments
            
        Returns:
            HttpResponse: The response to send to the client
        """
        if not request.user.is_staff:
            return HttpResponseForbidden("You don't have permission to delete rooms.")
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        """
        Returns the URL to redirect to after successful deletion.
        
        Returns:
            str: The URL to redirect to
        """
        return reverse('reservation:room_list')

class ReservationListView(LoginRequiredMixin, ListView):
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
        form_class: The form class to use for the form
    """
    model = Reservation
    template_name = 'reservation/reservation_form.html'
    form_class = ReservationForm
    
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
        Also checks for overlapping reservations and sends email notification.
        
        Args:
            form: The validated form instance
            
        Returns:
            HttpResponseRedirect: Redirects to the success URL
        """
        # Check for overlapping reservations
        overlapping = Reservation.objects.filter(
            room=self.get_room(),
            date=form.cleaned_data['date'],
            start_time__lt=form.cleaned_data['end_time'],
            end_time__gt=form.cleaned_data['start_time']
        )
        
        if overlapping.exists():
            form.add_error('start_time', 'This time slot overlaps with an existing reservation.')
            return self.form_invalid(form)
        
        form.instance.room = self.get_room()
        form.instance.user = self.request.user
        
        # Save the reservation
        response = super().form_valid(form)
        
        # Send email notification
        subject = f'New Reservation: {form.instance.title}'
        html_message = render_to_string('reservation/email/reservation_created.html', {
            'reservation': form.instance,
            'user': self.request.user,
        })
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=None,  # Uses DEFAULT_FROM_EMAIL
            recipient_list=[self.request.user.email],
            html_message=html_message,
        )
        
        return response
    
    def get_success_url(self):
        """
        Returns the URL to redirect to after successful form submission.
        
        Returns:
            str: The URL to redirect to
        """
        return reverse('reservation:room_detail', kwargs={'pk': self.kwargs['pk']})

class ReservationUpdateView(LoginRequiredMixin, UpdateView):
    """
    A view that handles updating existing room reservations.
    
    Attributes:
        model: The Reservation model to be used
        template_name: The template to render the form
        form_class: The form class to use for the form
    """
    model = Reservation
    template_name = 'reservation/reservation_form.html'
    form_class = ReservationForm
    
    def dispatch(self, request, *args, **kwargs):
        """
        Checks if the user has permission to update the reservation.
        
        Args:
            request: The HTTP request object
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments
            
        Returns:
            HttpResponse: The response to send to the client
        """
        reservation = self.get_object()
        if request.user != reservation.user:
            return HttpResponseForbidden("You don't have permission to edit this reservation.")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        """
        Adds the room object to the template context.
        
        Args:
            **kwargs: Additional context data
            
        Returns:
            dict: The context dictionary with the room object added
        """
        context = super().get_context_data(**kwargs)
        context['room'] = self.object.room
        return context
    
    def form_valid(self, form):
        """
        Checks for overlapping reservations before saving the update.
        
        Args:
            form: The validated form instance
            
        Returns:
            HttpResponseRedirect: Redirects to the success URL
        """
        # Check for overlapping reservations, excluding current reservation
        overlapping = Reservation.objects.filter(
            room=self.object.room,
            date=form.cleaned_data['date'],
            start_time__lt=form.cleaned_data['end_time'],
            end_time__gt=form.cleaned_data['start_time']
        ).exclude(pk=self.object.pk)
        
        if overlapping.exists():
            form.add_error('start_time', 'This time slot overlaps with an existing reservation.')
            return self.form_invalid(form)
        
        return super().form_valid(form)
    
    def get_success_url(self):
        """
        Returns the URL to redirect to after successful form submission.
        
        Returns:
            str: The URL to redirect to
        """
        return reverse('reservation:room_detail', kwargs={'pk': self.object.room.pk})

class ReservationDeleteView(LoginRequiredMixin, DeleteView):
    """View for deleting a reservation."""
    model = Reservation
    template_name = 'reservation/reservation_confirm_delete.html'

    def get_queryset(self):
        """Allow staff to delete any reservation, but regular users can only delete their own."""
        if self.request.user.is_staff:
            return Reservation.objects.all()
        return Reservation.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        """Store the referring page URL in session when showing the confirmation page."""
        if 'HTTP_REFERER' in request.META:
            request.session['reservation_delete_redirect'] = request.META['HTTP_REFERER']
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        """Return to the original listing page after successful deletion."""
        # Get and remove the stored URL from session
        redirect_url = self.request.session.pop('reservation_delete_redirect', None)
        
        # If no stored URL, redirect based on user type
        if not redirect_url or '/delete/' in redirect_url:
            if self.request.user.is_staff:
                return reverse('reservation:admin_reservation_list')
            return reverse('reservation:my_reservations')
            
        return redirect_url

class MyReservationListView(LoginRequiredMixin, ListView):
    """
    A view that displays all reservations created by the currently logged-in user.
    
    Attributes:
        model: The Reservation model to be used
        template_name: The template to render the list
        context_object_name: The name of the object list in the template
    """
    model = Reservation
    template_name = 'reservation/my_reservations.html'
    context_object_name = 'reservations'
    
    def get_queryset(self):
        """
        Returns a queryset of reservations created by the current user,
        ordered by date and start time.
        
        Returns:
            QuerySet: A filtered queryset containing the user's reservations
        """
        return Reservation.objects.filter(user=self.request.user).order_by('date', 'start_time')

class ReservationStatusUpdateView(LoginRequiredMixin, View):
    """
    A view that handles updating the status of a reservation.
    Only accepts POST requests and requires user authentication.
    """
    http_method_names = ['post']
    
    def post(self, request, pk):
        """
        Updates the status of a reservation if the user has permission
        and the new status is valid.
        
        Args:
            request: The HTTP request object
            pk: The primary key of the reservation
            
        Returns:
            HttpResponseRedirect: Redirects to the referring page or reservation list
        """
        reservation = get_object_or_404(Reservation, pk=pk)
        
        # Only allow status updates by the reservation owner or staff
        if request.user != reservation.user and not request.user.is_staff:
            raise PermissionDenied
        
        new_status = request.POST.get('status')
        if new_status in dict(Reservation.STATUS_CHOICES):
            reservation.status = new_status
            reservation.save()
        
        return redirect(request.META.get('HTTP_REFERER', reverse('reservation:my_reservations')))

class SignupView(FormView):
    """
    A view that handles user registration using Django's UserCreationForm.
    Automatically logs in the user after successful registration.
    """
    form_class = UserCreationForm
    template_name = 'reservation/signup.html'
    success_url = '/rooms/'
    
    def form_valid(self, form):
        """
        Creates a new user and logs them in after successful registration.
        
        Args:
            form: The validated form instance
            
        Returns:
            HttpResponseRedirect: Redirects to the success URL
        """
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

class AdminReservationListView(LoginRequiredMixin, ListView):
    """
    A view that displays all reservations in the system.
    Only accessible by staff users.
    
    Attributes:
        model: The Reservation model to be used
        template_name: The template to render the list
        context_object_name: The name of the object list in the template
    """
    model = Reservation
    template_name = 'reservation/admin_reservation_list.html'
    context_object_name = 'reservations'
    
    def dispatch(self, request, *args, **kwargs):
        """
        Checks if the user has staff permissions to view all reservations.
        
        Args:
            request: The HTTP request object
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments
            
        Returns:
            HttpResponse: The response to send to the client
        """
        if not request.user.is_staff:
            return HttpResponseForbidden("You don't have permission to view all reservations.")
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        """
        Returns a queryset of all reservations, ordered by date and start time.
        
        Returns:
            QuerySet: A queryset containing all reservations
        """
        return Reservation.objects.all().order_by('date', 'start_time')

class AdminReservationCreateView(LoginRequiredMixin, CreateView):
    """
    A view that allows staff users to create reservations on behalf of any user.
    
    Attributes:
        model: The Reservation model to be used
        template_name: The template to render the form
        form_class: The form class to use for the form
    """
    model = Reservation
    template_name = 'reservation/admin_reservation_form.html'
    form_class = AdminReservationForm
    
    def dispatch(self, request, *args, **kwargs):
        """
        Checks if the user has staff permissions to create reservations.
        
        Args:
            request: The HTTP request object
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments
            
        Returns:
            HttpResponse: The response to send to the client
        """
        if not request.user.is_staff:
            return HttpResponseForbidden("You don't have permission to create reservations on behalf of users.")
        return super().dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        """
        Adds the list of users and rooms to the template context.
        
        Args:
            **kwargs: Additional context data
            
        Returns:
            dict: The context dictionary with users and rooms added
        """
        context = super().get_context_data(**kwargs)
        context['users'] = User.objects.all().order_by('username')
        context['rooms'] = Room.objects.filter(is_active=True).order_by('name')
        return context
    
    def form_valid(self, form):
        """
        Checks for overlapping reservations before saving and sends email notification.
        
        Args:
            form: The validated form instance
            
        Returns:
            HttpResponseRedirect: Redirects to the success URL
        """
        # Check for overlapping reservations
        overlapping = Reservation.objects.filter(
            room=form.cleaned_data['room'],
            date=form.cleaned_data['date'],
            start_time__lt=form.cleaned_data['end_time'],
            end_time__gt=form.cleaned_data['start_time']
        )
        
        if overlapping.exists():
            form.add_error('start_time', 'This time slot overlaps with an existing reservation.')
            return self.form_invalid(form)
        
        # Save the reservation
        response = super().form_valid(form)
        
        # Send email notification
        subject = f'New Reservation: {form.instance.title}'
        html_message = render_to_string('reservation/email/reservation_created.html', {
            'reservation': form.instance,
            'user': form.instance.user,
        })
        plain_message = strip_tags(html_message)
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=None,  # Uses DEFAULT_FROM_EMAIL
            recipient_list=[form.instance.user.email],
            html_message=html_message,
        )
        
        return response
    
    def get_success_url(self):
        """
        Returns the URL to redirect to after successful form submission.
        
        Returns:
            str: The URL to redirect to
        """
        return reverse('reservation:admin_reservation_list')

def reserved_times(request):
    """
    Returns reserved time ranges for a given room and date as JSON.
    Expects 'room_id' and 'date' as GET parameters.
    Response format: [{"start": "HH:MM", "end": "HH:MM"}, ...]
    """
    room_id = request.GET.get('room_id')
    date = request.GET.get('date')
    if not room_id or not date:
        return JsonResponse({'error': 'Missing room_id or date parameter.'}, status=400)
    reservations = Reservation.objects.filter(room_id=room_id, date=date)
    data = [
        {'start': r.start_time.strftime('%H:%M'), 'end': r.end_time.strftime('%H:%M')}
        for r in reservations
    ]
    return JsonResponse(data, safe=False)

def available_dates(request):
    """
    Returns a list of available dates (YYYY-MM-DD) for a given room.
    For demo: next 30 days, dates not fully booked (at least one slot available).
    """
    room_id = request.GET.get('room_id')
    if not room_id:
        return JsonResponse({'error': 'Missing room_id parameter.'}, status=400)
    today = timezone.now().date()
    available = []
    for i in range(0, 30):
        d = today + datetime.timedelta(days=i)
        reservations = Reservation.objects.filter(room_id=room_id, date=d)
        # 09:00~18:00, 30분 단위 총 18개 슬롯
        if reservations.count() < 18:
            available.append(d.strftime('%Y-%m-%d'))
    return JsonResponse(available, safe=False)
