from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('landing/', views.land, name='land'),
    path('landing/<int:index>', views.landing, name='landing'),
]