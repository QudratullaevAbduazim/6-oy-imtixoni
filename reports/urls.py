from django.urls import path
from .views import ReportsView

urlpatterns = [
    path('analytics/', ReportsView.as_view(), name='reports'),
]