from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Room, Reservation
from .serializers import RoomSerializer, ReservationSerializer, UserSerializer, RegisterSerializer, CustomTokenObtainPairSerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from datetime import timedelta, datetime, time
from rest_framework import serializers
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.

class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class ReservationViewSet(viewsets.ModelViewSet):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return Reservation.objects.all()
        return Reservation.objects.filter(user=user)

    def perform_create(self, serializer):
        data = serializer.validated_data
        room = data.get("room")
        date = data.get("date")
        new_start_time = data.get("start_time")
        new_end_time = data.get("end_time")
        # Check for an overlapping reservation (same room, same date, and overlapping time range)
        overlap = Reservation.objects.filter(room=room, date=date).filter(
            start_time__lt=new_end_time, end_time__gt=new_start_time
        ).exists()
        if overlap:
            raise serializers.ValidationError("A reservation with overlapping time range already exists for this room and date.")
        serializer.save(user=self.request.user)

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

class CurrentUserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_staff": user.is_staff,
            "is_superuser": user.is_superuser,
        })

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]
    def get (self, request):
         serializer = UserSerializer(request.user)
         return Response(serializer.data)

class RegisterView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "user": UserSerializer(user).data,
                "message": "User Created Successfully"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class MyReservationsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        reservations = Reservation.objects.filter(user=request.user)
        serializer = ReservationSerializer(reservations, many=True)
        return Response(serializer.data)
