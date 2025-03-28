from django.urls import path
from . import views


urlpatterns = [
    path('register',views.signup, name= 'register'),
    path('profile/',views.profile, name='profile'),
]