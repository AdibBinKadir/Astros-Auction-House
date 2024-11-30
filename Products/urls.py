from django.urls import path, include
from . import views

urlpatterns = [
    path('<int:index>', views.products),
]