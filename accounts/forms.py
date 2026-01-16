# users/forms.py
from django import forms
from .models import Profile

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        # Faqat Profile modelida bor maydonlarni qoldiramiz
        fields = ['avatar']

def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")

        if avatar:
            if avatar.size > 2 * 1024 * 1024:  # 2 MB limit
                raise forms.ValidationError(
                    "Avatar hajmi 2MB dan oshmasligi kerak."
                )

        return avatar