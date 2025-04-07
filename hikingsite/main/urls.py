from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('trips/', views.trips, name='trips'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
