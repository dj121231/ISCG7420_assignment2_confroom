from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Room, Reservation
from datetime import date, time, timedelta
from django.core.management import call_command

class ReservationAPITests(TestCase):
    def setUp(self):
         call_command("migrate", verbosity=0)
         # Create users
         self.admin = User.objects.create_superuser(username="admin", email="admin@example.com", password="adminpass")
         self.user = User.objects.create_user(username="user", email="user@example.com", password="userpass")
         # Create a test room
         self.room = Room.objects.create(name="Test Room", capacity=10, location="Test Location")
         # Create API client
         self.client = APIClient()

    def test_obtain_jwt_token(self):
         """Test that a user can obtain a JWT token by posting to /api/token/."""
         url = "/api/token/"
         data = {"username": "user", "password": "userpass"}
         response = self.client.post(url, data, format="json")
         self.assertEqual(response.status_code, status.HTTP_200_OK, "Expected 200 OK when obtaining JWT token.")
         self.assertIn("access", response.data, "Expected 'access' token in response.")

    def test_create_reservation(self):
         """Test that a logged-in user can create a reservation via /api/reservations/."""
         # Authenticate the user (using JWT token) (simulated by force_authenticate for simplicity).
         self.client.force_authenticate(user=self.user)
         url = "/api/reservations/"
         data = {
             "room": self.room.id,
             "title": "Test Reservation",
             "date": date.today().isoformat(),
             "start_time": time(9, 0).isoformat(),
             "end_time": time(10, 0).isoformat(),
             "description": "Test reservation description"
         }
         response = self.client.post(url, data, format="json")
         self.assertEqual(response.status_code, status.HTTP_201_CREATED, "Expected 201 Created when creating a reservation.")
         self.assertEqual(Reservation.objects.count(), 1, "Expected one reservation to be created.")

    def test_overlapping_reservation_rejected(self):
         """Test that a reservation with an overlapping time (for the same room) is rejected."""
         # Authenticate the user (simulated by force_authenticate).
         self.client.force_authenticate(user=self.user)
         url = "/api/reservations/"
         # Create a reservation (for today, 9:00–10:00) (using the test room).
         data = {
             "room": self.room.id,
             "title": "First Reservation",
             "date": date.today().isoformat(),
             "start_time": time(9, 0).isoformat(),
             "end_time": time(10, 0).isoformat(),
             "description": "First reservation."
         }
         response = self.client.post(url, data, format="json")
         self.assertEqual(response.status_code, status.HTTP_201_CREATED, "Expected 201 Created for first reservation.")
         # Now, try to create a second reservation (for the same room, same date, overlapping time (9:30–10:30)).
         data = {
             "room": self.room.id,
             "title": "Overlapping Reservation",
             "date": date.today().isoformat(),
             "start_time": time(9, 30).isoformat(),
             "end_time": time(10, 30).isoformat(),
             "description": "Overlapping reservation."
         }
         response = self.client.post(url, data, format="json")
         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST, "Expected 400 Bad Request (overlapping reservation).")

    def test_only_logged_in_users_reservations_returned(self):
         """Test that only the logged-in user's reservations are returned from /api/reservations/."""
         # Authenticate the user (simulated by force_authenticate) and create a reservation.
         self.client.force_authenticate(user=self.user)
         url = "/api/reservations/"
         data = {
             "room": self.room.id,
             "title": "User Reservation",
             "date": date.today().isoformat(),
             "start_time": time(9, 0).isoformat(),
             "end_time": time(10, 0).isoformat(),
             "description": "User's reservation."
         }
         response = self.client.post(url, data, format="json")
         self.assertEqual(response.status_code, status.HTTP_201_CREATED, "Expected 201 Created for user's reservation.")
         # Authenticate as admin (simulated) and create a reservation (for the same room, but a different time).
         self.client.force_authenticate(user=self.admin)
         data = {
             "room": self.room.id,
             "title": "Admin Reservation",
             "date": date.today().isoformat(),
             "start_time": time(11, 0).isoformat(),
             "end_time": time(12, 0).isoformat(),
             "description": "Admin's reservation."
         }
         response = self.client.post(url, data, format="json")
         self.assertEqual(response.status_code, status.HTTP_201_CREATED, "Expected 201 Created for admin's reservation.")
         # Re-authenticate as the regular user and GET /api/reservations/.
         self.client.force_authenticate(user=self.user)
         response = self.client.get(url, format="json")
         self.assertEqual(response.status_code, status.HTTP_200_OK, "Expected 200 OK when fetching reservations.")
         self.assertEqual(len(response.data), 1, "Expected only one reservation (the user's) to be returned.")

    def test_unauthorized_access_returns_401(self):
         """Test that an unauthenticated user gets 401 Unauthorized when accessing /api/reservations/."""
         url = "/api/reservations/"
         response = self.client.get(url, format="json")
         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED, "Expected 401 Unauthorized for unauthenticated access.")

    def test_update_reservation(self):
         """Test that a logged-in user can update a reservation (via PUT /api/reservations/{id}/) and that the update is successful."""
         self.client.force_authenticate(user=self.user)
         url = f"/api/reservations/{self.reservation.id}/"
         data = { "room": self.room.id, "title": "Updated Reservation", "date": date.today().isoformat(), "start_time": time(11, 0).isoformat(), "end_time": time(12, 0).isoformat(), "description": "Updated reservation." }
         response = self.client.put(url, data, format="json")
         self.assertEqual(response.status_code, status.HTTP_200_OK, "Expected 200 OK when updating a reservation.")
         self.reservation.refresh_from_db()
         self.assertEqual(self.reservation.title, "Updated Reservation", "Expected reservation title to be updated.")

    def test_delete_reservation(self):
         """Test that a logged-in user can delete a reservation (via DELETE /api/reservations/{id}/) and that it is removed from the database."""
         self.client.force_authenticate(user=self.user)
         url = f"/api/reservations/{self.reservation.id}/"
         response = self.client.delete(url, format="json")
         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT, "Expected 204 No Content when deleting a reservation.")
         self.assertFalse(Reservation.objects.filter(id=self.reservation.id).exists(), "Expected reservation to be removed from the database.")

    def test_get_queryset(self):
         """Test that a superuser (admin) sees all reservations (via GET /api/reservations/) while a regular user (user) sees only their own."""
         # (self.reservation is created for self.user in setUp.)
         # Authenticate as admin and GET /api/reservations/.
         self.client.force_authenticate(user=self.admin)
         url = "/api/reservations/"
         response = self.client.get(url, format="json")
         self.assertEqual(response.status_code, status.HTTP_200_OK, "Expected 200 OK when admin fetches reservations.")
         self.assertEqual(len(response.data), 1, "Expected admin to see one reservation (the one created in setUp).")
         # Authenticate as the regular user (self.user) and GET /api/reservations/.
         self.client.force_authenticate(user=self.user)
         response = self.client.get(url, format="json")
         self.assertEqual(response.status_code, status.HTTP_200_OK, "Expected 200 OK when user fetches reservations.")
         self.assertEqual(len(response.data), 1, "Expected user to see only their own reservation (the one created in setUp).")
