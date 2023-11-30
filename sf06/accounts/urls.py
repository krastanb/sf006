from django.urls import path, include
from django.contrib.auth.views import LoginView
from .views import *

urlpatterns = [
    path('signup', SignUp.as_view(), name='signup'),
    path('login', LoginView.as_view(template_name='login.html'), name='login')
    ]