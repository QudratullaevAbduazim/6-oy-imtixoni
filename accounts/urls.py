from django.urls import path

from reports import views
from .views import AccountUpdateView, DashboardView, AccountCreateView, AccountListView


urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('my-accounts/', AccountListView.as_view(), name='account_list'),
    path('account/add/', AccountCreateView.as_view(), name='account_create'),
    path('account/<int:pk>/edit/', AccountUpdateView.as_view(), name='account_update'),
]