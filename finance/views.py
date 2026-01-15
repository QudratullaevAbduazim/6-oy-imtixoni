from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from .models import Account, Category, Transaction

# 1. Dashboard - Hamma narsani hisoblab ko'rsatuvchi asosiy sahifa
class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        accounts = Account.objects.filter(user=user)
        
        # Jami balansni hisoblash (hamma hamyonlardagi pul yig'indisi)
        total_balance = accounts.aggregate(Sum('balance'))['balance__sum'] or 0
        
        # Oxirgi 10 ta tranzaksiyani olish
        transactions = Transaction.objects.filter(user=user).order_by('-date')[:10]
        
        context = {
            'accounts': accounts,
            'total_balance': total_balance,
            'transactions': transactions,
        }
        return render(request, 'finance/dashboard.html', context)

# 2. Hisob yaratish (Karta, Naqd pul va h.k.)
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

# 3. Tranzaksiya yaratish (Kirim-chiqim amali)
class TransactionCreateView(LoginRequiredMixin, View):
    def get(self, request):
        # HTML dagi <select> uchun userga tegishli account va kategorylarni yuboramiz
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
        amount = float(request.POST.get('amount', 0))
        comment = request.POST.get('comment', '')

        # Bazadan tegishli ob'ektlarni olamiz
        account = get_object_or_404(Account, id=account_id, user=request.user)
        category = get_object_or_404(Category, id=category_id, user=request.user)

        # 1. Tranzaksiyani yaratish
        Transaction.objects.create(
            user=request.user,
            account=account,
            category=category,
            amount=amount,
            comment=comment
        )

        # 2. MANTIQ: Account balansini yangilash
        if category.kind == 'out':
            account.balance -= amount  # Chiqim bo'lsa ayiramiz
        else:
            account.balance += amount  # Kirim bo'lsa qo'shamiz
        
        account.save() # Yangilangan balansni bazaga saqlaymiz
        
        return redirect('dashboard')