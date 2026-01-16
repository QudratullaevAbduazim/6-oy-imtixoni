from django.db import models
from django.contrib.auth.models import User
from accounts.models import Account

class Category(models.Model):
    KIND_CHOICES = [
        ('in', 'Kirim (Income)'),
        ('out', 'Chiqim (Expense)'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    kind = models.CharField(max_length=3, choices=KIND_CHOICES)
    icon = models.CharField(max_length=50, blank=True) 

    def __str__(self):
        return f"{self.name} ({self.get_kind_display()})"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    
    amount = models.DecimalField(max_digits=20, decimal_places=2)  
    currency = models.CharField(max_length=3)  
    
    exchange_rate = models.DecimalField(max_digits=10, decimal_places=2, default=12800)
    
    amount_in_uzs = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    
    comment = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    
    is_transfer = models.BooleanField(default=False)
    to_account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True, related_name='transfers_in')
    original_amount = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
    original_currency = models.CharField(max_length=3, null=True, blank=True)

    def __str__(self):
        return f"{self.account.name} | {self.amount} {self.currency}"
