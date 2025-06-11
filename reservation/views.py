from django.shortcuts import render
from rest_framework import viewsets
from .models import Room, Reservation
from .serializers import RoomSerializer, ReservationSerializer, UserSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from datetime import timedelta, datetime, time

# Create your views here.

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None):
        reservation = self.get_object()
        reservation.status = 'confirmed'
        reservation.save()
        serializer = self.get_serializer(reservation)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def reject(self, request, pk=None):
        reservation = self.get_object()
        reservation.status = 'cancelled'
        reservation.save()
        serializer = self.get_serializer(reservation)
        return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

class get_reserved_times(APIView):
    def get(self, request):
        room = request.query_params.get('room')
        date = request.query_params.get('date')
        if not (room and date):
             return Response({"error": "Query parameters 'room' and 'date' are required."}, status=400)
        try:
             date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        except ValueError:
             return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=400)
        reservations = Reservation.objects.filter(room=room, date=date_obj)
        reserved_times = [{"start_time": res.start_time, "end_time": res.end_time} for res in reservations]
        return Response(reserved_times)

class get_available_dates(APIView):
    def get(self, request):
         room = request.query_params.get('room')
         if not room:
             return Response({"error": "Query parameter 'room' is required."}, status=400)
         today = timezone.now().date()
         end_date = today + timedelta(days=14)
         available_dates = []
         current = today
         while current <= end_date:
             # (Assume a day is fully booked if every 30-min slot (from 9:00 to 18:00) is reserved.)
             # (In a real scenario, you might compute a list of all 30-min slots (e.g. 9:00, 9:30, ..., 17:30) and then check if any slot is free.)
             # (For simplicity, we assume that if there is at least one reservation on that day, the day is fully booked.)
             if not Reservation.objects.filter(room=room, date=current).exists():
                 available_dates.append(current.strftime("%Y-%m-%d"))
             current += timedelta(days=1)
         return Response(available_dates)
