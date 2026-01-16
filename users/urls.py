from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    RegisterView, LoginView, ProfileView, 
    ProfileUpdateView, ChangePasswordView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('profile/', ProfileView.as_view(), name='profile_view'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('profile/password/', ChangePasswordView.as_view(), name='password_change'),
]