from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    ACCOUNT_TYPES = [
        ('CASH', 'Naqd pul'),
        ('CARD', 'Bank kartasi'),
        ('OTHER', 'Boshqa'),
    ]
    CURRENCIES = [
        ('UZS', "O'zbek so'mi"),
        ('USD', "AQSH Dollari"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    name = models.CharField(max_length=100) 
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES, default='CARD')
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, choices=CURRENCIES, default='UZS')
    icon = models.CharField(max_length=50, default='wallet') 

    def __str__(self):
        return f"{self.name} - {self.balance} {self.currency}"