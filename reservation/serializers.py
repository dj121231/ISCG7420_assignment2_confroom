from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Room, Reservation
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ReservationSerializer(serializers.ModelSerializer):
    # Make room writable (accepts pk from POST), user remains read-only
    room = serializers.PrimaryKeyRelatedField(queryset=Room.objects.all())
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = ["id", "user", "status", "created_at", "updated_at"]

    def validate(self, data):
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        room = data.get('room')
        date = data.get('date')
        instance = getattr(self, 'instance', None)

        # 1. start_time < end_time
        if start_time and end_time and start_time >= end_time:
            raise serializers.ValidationError('start_time must be before end_time.')

        # 2. Times between 09:00 and 18:00
        for t, label in [(start_time, 'start_time'), (end_time, 'end_time')]:
            if t:
                if t.hour < 9 or t.hour > 18 or (t.hour == 18 and t.minute > 0):
                    raise serializers.ValidationError(f'{label} must be between 09:00 and 18:00.')
                if t.minute not in (0, 30):
                    raise serializers.ValidationError(f'{label} must be on a 30-minute interval (minutes 0 or 30).')

        # 3. No overlapping reservations
        if room and date and start_time and end_time:
            qs = Reservation.objects.filter(room=room, date=date)
            if instance:
                qs = qs.exclude(pk=instance.pk)
            for res in qs:
                if res.start_time < end_time and res.end_time > start_time:
                    raise serializers.ValidationError('Overlapping reservation exists for this room, date, and time.')

        return data 

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    role = serializers.ChoiceField(choices=[('user', 'User'), ('admin', 'Admin')], default='user', write_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'role')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        role = validated_data.pop('role', 'user')
        validated_data.pop('password2')
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        if role == 'admin':
            user.is_staff = True
            user.save()
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims to the token
        token['username'] = user.username
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Add extra responses here
        data['username'] = self.user.username
        data['is_staff'] = self.user.is_staff
        data['is_superuser'] = self.user.is_superuser
        return data 