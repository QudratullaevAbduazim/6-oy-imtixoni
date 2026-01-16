from django.contrib import admin
from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    # Admin panelda ko‘rinadigan ustunlar
    list_display = ('id', 'user', 'name', 'account_type', 'balance', 'currency', 'icon')
    
    # Qidirish uchun maydonlar
    search_fields = ('name', 'user__username')
    
    # Filtrlash uchun maydonlar
    list_filter = ('account_type', 'currency')
    
    # Tartiblash
    ordering = ('-id',)
    
    # Har bir sahifada yozuvlar soni
    list_per_page = 25
