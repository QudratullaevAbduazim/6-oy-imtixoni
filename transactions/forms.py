from django import forms
from django.core.exceptions import ValidationError
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['account', 'category', 'amount', 'comment']

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        
        if amount is not None and amount <= 0:
            raise ValidationError("Tranzaktsiya miqdori 0 dan katta bo'lishi kerak.")
        
        return amount

    def clean(self):
        cleaned_data = super().clean()
        account = cleaned_data.get('account')
        amount = cleaned_data.get('amount')

        if account and amount:
            if account.balance < amount:
                raise ValidationError({
                    'amount': f"Hisobda mablag' yetarli emas. Joriy balans: {account.balance}"
                })
        
        return cleaned_data