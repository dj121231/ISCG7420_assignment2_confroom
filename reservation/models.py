from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

# Models for the reservation system

class Room(models.Model):
    """
    Room model represents a bookable room in the system
    Contains information about room characteristics and status
    """
    # Basic room information
    name = models.CharField(max_length=100)  # Name of the room
    capacity = models.IntegerField(validators=[MinValueValidator(1)])  # Maximum number of people allowed
    description = models.TextField(blank=True)  # Detailed description of the room
    location = models.CharField(max_length=200)  # Physical location of the room
    facilities = models.TextField(blank=True)  # Available facilities in the room
    
    # Room status
    is_active = models.BooleanField(default=True)  # Whether the room is available for booking
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)  # When the room was added to system
    updated_at = models.DateTimeField(auto_now=True)  # When the room was last modified

    def __str__(self):
        """Returns string representation of the room"""
        return self.name

class Reservation(models.Model):
    """
    Reservation model represents a booking of a room
    Tracks who booked what room and when
    """
    # Status options for reservations
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    # Relationship fields
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='reservations')  # Room being reserved
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations')  # User making reservation
    
    # Reservation details
    title = models.CharField(max_length=200)  # Title/purpose of reservation
    description = models.TextField(blank=True)  # Additional details about reservation
    date = models.DateField()  # Date of reservation
    start_time = models.TimeField()  # Start time of reservation
    end_time = models.TimeField()  # End time of reservation
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')  # Current status
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)  # When reservation was created
    updated_at = models.DateTimeField(auto_now=True)  # When reservation was last modified

    class Meta:
        """Meta options for Reservation model"""
        ordering = ['date', 'start_time']  # Default ordering by date and start time

    def __str__(self):
        """Returns string representation of the reservation"""
        return f"{self.room.name} - {self.title} by {self.user.username} on {self.date}"
