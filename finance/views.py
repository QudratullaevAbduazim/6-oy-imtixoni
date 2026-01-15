from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from .models import Account, Category, Transaction

# 1. Dashboard - LoginRequiredMixin qaytarildi
from django.views import View
from django.db.models import Sum
from .models import Account, Transaction

class DashboardView(View):
    def get(self, request):
        # Agar foydalanuvchi tizimga kirmagan bo'lsa, uni to'g'ri manzilga yuboramiz
        if not request.user.is_authenticated:
            return redirect('login') # Settingsdagi LOGIN_URL ni aylanib o'tamiz
            
        user = request.user
        accounts = Account.objects.filter(user=user)
        total_balance = accounts.aggregate(Sum('balance'))['balance__sum'] or 0
        transactions = Transaction.objects.filter(user=user).order_by('-date')[:10]
        
        context = {
            'accounts': accounts,
            'total_balance': total_balance,
            'transactions': transactions,
        }
        return render(request, 'templates/dashboard.html', context)

# 2. Hisob yaratish
class AccountCreateView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'finance/account_form.html')

    def post(self, request):
        name = request.POST.get('name')
        balance = request.POST.get('balance', 0)
        
        Account.objects.create(
            user=request.user,
            name=name,
            balance=balance
        )
        return redirect('dashboard')

# 3. Tranzaksiya yaratish
class TransactionCreateView(LoginRequiredMixin, View):
    def get(self, request):
        accounts = Account.objects.filter(user=request.user)
        categories = Category.objects.filter(user=request.user)
        
        context = {
            'accounts': accounts,
            'categories': categories
        }
        return render(request, 'finance/transaction_form.html', context)

    def post(self, request):
        account_id = request.POST.get('account')
        category_id = request.POST.get('category')
        amount_str = request.POST.get('amount', '0')
        
        # Bo'sh qiymat kelib qolsa xato bermasligi uchun
        amount = float(amount_str) if amount_str else 0
        comment = request.POST.get('comment', '')

        account = get_object_or_404(Account, id=account_id, user=request.user)
        category = get_object_or_404(Category, id=category_id, user=request.user)

        Transaction.objects.create(
            user=request.user,
            account=account,
            category=category,
            amount=amount,
            comment=comment
        )

        if category.kind == 'out':
            account.balance -= amount
        else:
            account.balance += amount
        
        account.save()
        return redirect('dashboard')