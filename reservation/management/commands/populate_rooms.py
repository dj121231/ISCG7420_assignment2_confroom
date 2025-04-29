from django.core.management.base import BaseCommand
from reservation.models import Room

class Command(BaseCommand):
    """
    A management command that populates the database with 10 conference rooms
    if they don't already exist.
    """
    help = 'Populates the database with 10 conference rooms'

    def handle(self, *args, **options):
        """
        Creates 10 conference rooms if they don't exist.
        
        Args:
            *args: Additional positional arguments
            **options: Additional keyword arguments
        """
        # List of room data
        rooms_data = [
            {
                'name': 'Room A',
                'capacity': 10,
                'location': 'First Floor',
                'description': 'This is Room A, a small meeting room suitable for up to 10 people.',
                'is_active': True
            },
            {
                'name': 'Room B',
                'capacity': 15,
                'location': 'First Floor',
                'description': 'This is Room B, a medium-sized meeting room suitable for up to 15 people.',
                'is_active': True
            },
            {
                'name': 'Room C',
                'capacity': 20,
                'location': 'First Floor',
                'description': 'This is Room C, a large meeting room suitable for up to 20 people.',
                'is_active': True
            },
            {
                'name': 'Room D',
                'capacity': 8,
                'location': 'Second Floor',
                'description': 'This is Room D, a small meeting room suitable for up to 8 people.',
                'is_active': True
            },
            {
                'name': 'Room E',
                'capacity': 12,
                'location': 'Second Floor',
                'description': 'This is Room E, a medium-sized meeting room suitable for up to 12 people.',
                'is_active': True
            },
            {
                'name': 'Room F',
                'capacity': 25,
                'location': 'Second Floor',
                'description': 'This is Room F, a large meeting room suitable for up to 25 people.',
                'is_active': True
            },
            {
                'name': 'Room G',
                'capacity': 6,
                'location': 'Third Floor',
                'description': 'This is Room G, a small meeting room suitable for up to 6 people.',
                'is_active': True
            },
            {
                'name': 'Room H',
                'capacity': 18,
                'location': 'Third Floor',
                'description': 'This is Room H, a medium-sized meeting room suitable for up to 18 people.',
                'is_active': True
            },
            {
                'name': 'Room I',
                'capacity': 30,
                'location': 'Third Floor',
                'description': 'This is Room I, a large meeting room suitable for up to 30 people.',
                'is_active': True
            },
            {
                'name': 'Room J',
                'capacity': 40,
                'location': 'Fourth Floor',
                'description': 'This is Room J, a conference room suitable for up to 40 people.',
                'is_active': True
            }
        ]

        # Create rooms if they don't exist
        for room_data in rooms_data:
            room, created = Room.objects.get_or_create(
                name=room_data['name'],
                defaults={
                    'capacity': room_data['capacity'],
                    'location': room_data['location'],
                    'description': room_data['description'],
                    'is_active': room_data['is_active']
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully created room "{room.name}"')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Room "{room.name}" already exists')
                ) 