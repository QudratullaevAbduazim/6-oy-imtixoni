from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.name} - {self.balance}"

class Category(models.Model):
    KIND_CHOICES = [('in', 'Kirim'), ('out', 'Chiqim')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    kind = models.CharField(max_length=3, choices=KIND_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.get_kind_display()})"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    comment = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)