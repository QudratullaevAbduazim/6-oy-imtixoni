# accounts/admin.py
from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # Admin panelda ko‘rinadigan ustunlar
    list_display = ('id', 'user', 'language', 'preferred_currency', 'avatar')
    
    # Qidirish uchun maydonlar
    search_fields = ('user__username', 'preferred_currency')
    
    # Filtrlash uchun maydonlar
    list_filter = ('language', 'preferred_currency')
    
    # Tartiblash
    ordering = ('user__username',)
    
    # readonly_fields → faqat ko‘rish uchun
    readonly_fields = ('avatar',)
    
    # Har bir sahifada yozuvlar soni
    list_per_page = 25
