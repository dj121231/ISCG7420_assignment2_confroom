from django.contrib import admin
from .models import Room, Reservation

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Room model.
    Provides a user-friendly interface for managing meeting rooms.
    """
    # Fields to display in the list view
    list_display = ('name', 'capacity', 'location', 'is_active', 'created_at')
    
    # Fields that can be searched in the admin interface
    search_fields = ('name', 'location', 'description', 'facilities')
    
    # Fields that can be used to filter the list view
    list_filter = ('is_active', 'capacity')
    
    # Fields that should be read-only in the admin interface
    readonly_fields = ('created_at', 'updated_at')
    
    # Group fields into sections in the detail view
    fieldsets = (
        # Basic information section
        ('Basic Information', {
            'fields': ('name', 'capacity', 'location')
        }),
        # Additional information section (collapsible)
        ('Additional Information', {
            'fields': ('description', 'facilities'),
            'classes': ('collapse',)  # Makes this section collapsible
        }),
        # Status section
        ('Status', {
            'fields': ('is_active',)
        }),
        # Timestamps section (collapsible)
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Makes this section collapsible
        })
    )

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Reservation model.
    Provides a user-friendly interface for managing room reservations.
    """
    # Fields to display in the list view
    list_display = ('room', 'user', 'title', 'date', 'start_time', 'end_time', 'status')
    
    # Fields that can be searched in the admin interface
    # Note: room__name and user__username use related field lookups
    search_fields = ('room__name', 'user__username', 'title', 'description')
    
    # Fields that can be used to filter the list view
    list_filter = ('status', 'date', 'room')
    
    # Fields that should be read-only in the admin interface
    readonly_fields = ('created_at', 'updated_at')
    
    # Group fields into sections in the detail view
    fieldsets = (
        # Reservation details section
        ('Reservation Details', {
            'fields': ('room', 'user', 'title', 'description')
        }),
        # Time information section
        ('Time Information', {
            'fields': ('date', 'start_time', 'end_time')
        }),
        # Status section
        ('Status', {
            'fields': ('status',)
        }),
        # Timestamps section (collapsible)
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # Makes this section collapsible
        })
    )
