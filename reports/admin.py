# reports/admin.py
from django.contrib import admin
from .models import CurrencyRate

@admin.register(CurrencyRate)
class CurrencyRateAdmin(admin.ModelAdmin):
    # Admin panelda ko‘rinadigan ustunlar
    list_display = ('id', 'code', 'rate', 'updated_at')
    
    # Qidirish uchun maydonlar
    search_fields = ('code',)
    
    # Filtrlash uchun maydonlar
    list_filter = ('updated_at',)
    
    # Tartiblash
    ordering = ('-updated_at',)
    
    # Har bir sahifada yozuvlar soni
    list_per_page = 25
