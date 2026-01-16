from django.contrib import admin
from .models import CurrencyRate

@admin.register(CurrencyRate)
class CurrencyRateAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'rate', 'updated_at')
    
    search_fields = ('code',)
    
    list_filter = ('updated_at',)
    
    ordering = ('-updated_at',)
    
    list_per_page = 25
