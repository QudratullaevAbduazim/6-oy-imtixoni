from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView
from django.utils import timezone
from decimal import Decimal, ROUND_DOWN 

from .models import Account
from transactions.models import Transaction, Category

USD_TO_UZS = Decimal('12800')

class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        accounts = request.user.accounts.all()
        transactions = Transaction.objects.filter(user=request.user).order_by('-date')[:15]

        total_balance_uzs = Decimal('0')
        total_income = Decimal('0')
        total_expense = Decimal('0')

        for acc in accounts:
            if acc.currency == 'USD':
                total_balance_uzs += (acc.balance * USD_TO_UZS)
            else:
                total_balance_uzs += acc.balance

        all_stats = Transaction.objects.filter(user=request.user, is_transfer=False)
        for t in all_stats:
            val = t.amount * USD_TO_UZS if t.currency == 'USD' else t.amount
            
            if t.category and t.category.kind == 'in':
                total_income += val
            elif t.category and t.category.kind == 'out':
                total_expense += val

        total_balance_usd = (total_balance_uzs / USD_TO_UZS).quantize(Decimal('0.01'), rounding=ROUND_DOWN)

        context = {
            'accounts': accounts,
            'transactions': transactions,
            'balance': total_balance_uzs.quantize(Decimal('1')),
            'total_income': total_income.quantize(Decimal('1')),
            'total_expense': total_expense.quantize(Decimal('1')),
            'total_balance_usd': total_balance_usd,
        }
        return render(request, 'accounts/dashboard.html', context)

class AccountCreateView(LoginRequiredMixin, CreateView):
    model = Account
    fields = ['name', 'account_type', 'balance', 'currency']
    template_name = 'accounts/account_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = Account
    fields = ['name', 'balance']
    template_name = 'accounts/account_form.html'
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)
    


class AccountListView(LoginRequiredMixin, View):
    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        
        
        total_balance_uzs = sum(
            acc.balance if acc.currency == 'UZS' else acc.balance * Decimal('12800') 
            for acc in accounts
        )
        
        return render(request, 'accounts/my_accounts.html', {
            'accounts': accounts,
            'total_balance_uzs': total_balance_uzs,
        })