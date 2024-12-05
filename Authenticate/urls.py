from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_user),
    path('logout_user/', views.logout_user),
    path('register_user/', views.register_user),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('reset_password/<uidb64>/<token>/', views.reset_password, name='reset_password'),
    path('forgot_password/', views.forgotpassword),

]
