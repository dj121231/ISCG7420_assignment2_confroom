from django import forms
from .models import Reservation, Room
from django.contrib.auth.models import User

# Helper to generate 30-min interval choices
TIME_CHOICES = [
    (f'{h:02d}:{m:02d}', f'{h:02d}:{m:02d}')
    for h in range(9, 18) for m in (0, 30)
] + [('18:00', '18:00')]

class ReservationForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    start_time = forms.ChoiceField(choices=TIME_CHOICES, widget=forms.Select)
    end_time = forms.ChoiceField(choices=TIME_CHOICES, widget=forms.Select)

    class Meta:
        model = Reservation
        fields = ['title', 'description', 'date', 'start_time', 'end_time']

class AdminReservationForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=User.objects.all(), widget=forms.Select)
    room = forms.ModelChoiceField(queryset=Room.objects.filter(is_active=True), widget=forms.Select)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    start_time = forms.ChoiceField(choices=TIME_CHOICES, widget=forms.Select)
    end_time = forms.ChoiceField(choices=TIME_CHOICES, widget=forms.Select)

    class Meta:
        model = Reservation
        fields = ['user', 'room', 'title', 'description', 'date', 'start_time', 'end_time'] 