from django.db import models

class CurrencyRate(models.Model):
    code = models.CharField(max_length=3, unique=True) 
    rate = models.DecimalField(max_digits=10, decimal_places=2) 
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"1 {self.code} = {self.rate} UZS"