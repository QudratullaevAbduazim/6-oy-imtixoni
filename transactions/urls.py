from django.urls import path
from .views import TransactionCreateView, TransferView, CategoryCreateView

urlpatterns = [
    path('add/<str:kind>/', TransactionCreateView.as_view(), name='transaction_add'),
    path('transfer/', TransferView.as_view(), name='transfer'),
    path('category/add/', CategoryCreateView.as_view(), name='category_create'),
]