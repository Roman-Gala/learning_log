"""URL paths for users."""

from django.urls import path, include

from . import views


app_name = 'users'
urlpatterns = [
    # Include default auth urls
    path('', include('django.contrib.auth.urls')),
    # Register
    path('register/', views.Register.as_view(), name='register'),
]
