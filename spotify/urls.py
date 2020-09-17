from django.urls import path

from . import views

urlpatterns = [
    path('auth/callback/', views.get_authorization_code),
    path('api/artists/', views.get_artists)
]
