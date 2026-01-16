import os
from django import forms
from django.core.exceptions import ValidationError
from django.conf import settings
from django.utils.translation import gettext_lazy as _  # TARJIMA UCHUN KERAK
from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'language', 'preferred_currency']
        # MAYDON NOMLARINI TARJIMA QILISH
        labels = {
            'avatar': _("Profil rasmi"),
            'language': _("Til"),
            'preferred_currency': _("Asosiy valyuta"),
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar and hasattr(avatar, 'size'):
            if avatar.name in ['avatars/default.jpg', 'avatars/default.png']:
                return avatar
            
            try:
                # Xatolik xabarini tarjimaga olish
                if avatar.size > 2 * 1024 * 1024:
                    raise forms.ValidationError(_("Rasm hajmi 2MB dan oshmasligi kerak!"))
            except (FileNotFoundError, OSError):
                return avatar
        return avatar

    def clean_language(self):
        language = self.cleaned_data.get('language')
        available_languages = [lang[0] for lang in settings.LANGUAGES]
        if language not in available_languages:
            # Xatolik xabarini tarjimaga olish
            raise ValidationError(_("Tanlangan til tizimda mavjud emas."))
        return language

    def clean_preferred_currency(self):
        currency = self.cleaned_data.get('preferred_currency')
        valid_currencies = ['UZS', 'USD']
        if currency not in valid_currencies:
            # Xatolik xabarini tarjimaga olish
            raise ValidationError(_("Noto'g'ri valyuta tanlandi."))
        return currency