from django.urls import path
from .views import DashboardView, AccountCreateView, TransactionCreateView

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('account/add/', AccountCreateView.as_view(), name='account_add'),
    path('transaction/add/', TransactionCreateView.as_view(), name='transaction_add'),
]