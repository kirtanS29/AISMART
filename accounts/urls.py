from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    
    path('verify-otp/', views.verify_otp_view, name='verify_otp'),
]


# This file defines the URL patterns for the accounts app, which handles user authentication.
# It includes paths for user signup, login, and logout, linking them to their respective views.