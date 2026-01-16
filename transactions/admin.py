# reports/admin.py
from django.contrib import admin
from .models import Category, Transaction

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    # Admin panelda ko‘rinadigan ustunlar
    list_display = ('id', 'user', 'name', 'kind', 'icon')
    
    # Qidirish uchun maydonlar
    search_fields = ('name', 'user__username')
    
    # Filtrlash uchun maydonlar
    list_filter = ('kind', 'user')
    
    # Tartiblash
    ordering = ('name',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    # Admin panelda ko‘rinadigan ustunlar
    list_display = (
        'id', 'user', 'account', 'category', 
        'amount', 'currency', 'exchange_rate', 
        'is_transfer', 'to_account', 'date'
    )
    
    # Qidirish uchun maydonlar
    search_fields = ('account__name', 'category__name', 'user__username', 'comment')
    
    # Filtrlash uchun maydonlar
    list_filter = ('currency', 'is_transfer', 'date', 'category')
    
    # Tartiblash
    ordering = ('-date',)
    
    # readonly_fields → faqat ko‘rish uchun
    readonly_fields = ('date',)
    
    # Sahifada yozuvlar soni
    list_per_page = 25

    def amount_with_currency(self, obj):
        return f"{obj.amount} {obj.currency}"
    amount_with_currency.short_description = "Summa"
