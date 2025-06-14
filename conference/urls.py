from django.contrib import admin
from django.http import HttpResponse
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.http import JsonResponse

# Root path response for base URL access (e.g., http://127.0.0.1:8000/)
def root_view(request):
    html = """
    <html>
    <head>
        <title>Welcome</title>
        <style>
            body {
                font-family: sans-serif;
                background-color: #121212;
                color: white;
                text-align: center;
                padding-top: 50px;
            }
            a.button {
                display: inline-block;
                margin: 10px;
                padding: 12px 24px;
                background-color: #1e88e5;
                color: white;
                text-decoration: none;
                border-radius: 8px;
                font-weight: bold;
            }
            a.button:hover {
                background-color: #1565c0;
            }
        </style>
    </head>
    <body>
        <h1>Welcome to the Conference Room Reservation API</h1>
        <a class="button" href="/admin/">Admin</a>
        <a class="button" href="/api/">API</a>
        <a class="button" href="/api/token/">Token (Login)</a>
        <a class="button" href="/api/token/refresh/">Token Refresh</a>
    </body>
    </html>
    """
    return HttpResponse(html)

urlpatterns = [
    path('', root_view),  # Root endpoint returns a simple welcome message
    path('admin/', admin.site.urls),  # Django admin panel
    path('api/', include('reservation.urls')),  # Reservation API routes
    
]
