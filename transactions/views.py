from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import transaction as db_transaction
from decimal import Decimal, ROUND_DOWN
from django.utils import timezone

from .models import Transaction, Category
from accounts.models import Account

# Kursni o'zgaruvchi sifatida saqlaymiz
USD_TO_UZS = Decimal('12800')

# ===================== 1. DASHBOARD (ASOSIY SAHIFA) =====================
# BU KLASS FAQAT DASHBOARD UCHUN JAVOB BERADI
# views.py



# ===================== 2. KIRIM / CHIQIM QO'SHISH =====================
class TransactionCreateView(LoginRequiredMixin, View):
    def get(self, request, kind):
        # Bu metod faqat forma sahifasini ochadi
        accounts = request.user.accounts.all()
        categories = Category.objects.filter(kind=kind)
        return render(request, 'transactions/transaction_form.html', {
            'kind': kind,
            'accounts': accounts,
            'categories': categories,
            'now': timezone.now()
        })

    def post(self, request, kind):
        account_id = request.POST.get('account')
        category_id = request.POST.get('category')
        amount = Decimal(request.POST.get('amount', 0))
        currency = request.POST.get('currency', 'UZS')
        comment = request.POST.get('comment', '')
        date = request.POST.get('date') or timezone.now()

        account = get_object_or_404(Account, id=account_id, user=request.user)
        category = get_object_or_404(Category, id=category_id)

        # Hamyon balansi uchun konvertatsiya
        amount_for_account = amount
        if currency != account.currency:
            if currency == 'USD' and account.currency == 'UZS':
                amount_for_account = (amount * USD_TO_UZS).quantize(Decimal('1'), rounding=ROUND_DOWN)
            elif currency == 'UZS' and account.currency == 'USD':
                amount_for_account = (amount / USD_TO_UZS).quantize(Decimal('0.01'), rounding=ROUND_DOWN)

        # --- PULNI TEKSHIRISH (YANGI QISM) ---
        if kind == 'out' and account.balance < amount_for_account:
            messages.error(request, "Hisobingizda mablag' yetarli emas!")
            # Qaytadan forma sahifasini yuklaymiz (xatolik xabari bilan)
            accounts = request.user.accounts.all()
            categories = Category.objects.filter(kind=kind)
            return render(request, 'transactions/transaction_form.html', {
                'kind': kind,
                'accounts': accounts,
                'categories': categories,
                'now': timezone.now(),
                'error': "Mablag' yetarli emas" # ixtiyoriy
            })
        # -------------------------------------

        with db_transaction.atomic():
            Transaction.objects.create(
                user=request.user, account=account, category=category,
                amount=amount, currency=currency,
                amount_in_uzs=(amount * USD_TO_UZS if currency == 'USD' else amount),
                comment=comment, date=date
            )
            # Balansni yangilash
            if kind == 'in':
                account.balance += amount_for_account
            else:
                account.balance -= amount_for_account
            account.save()

        messages.success(request, "Amal muvaffaqiyatli bajarildi!")
        return redirect('dashboard')

# ===================== 3. TRANSFER =====================
class TransferView(LoginRequiredMixin, View):
    def get(self, request):
        accounts = request.user.accounts.all()
        return render(request, 'transactions/transfer_form.html', {
            'accounts': accounts,
            'now': timezone.now()
        })

    def post(self, request):
        from_acc_id = request.POST.get('from_account')
        to_acc_id = request.POST.get('to_account')
        amount = Decimal(request.POST.get('amount', '0'))
        currency = request.POST.get('currency', 'UZS') # O'tkazilayotgan summa valyutasi
        date = request.POST.get('date') or timezone.now()

        from_account = get_object_or_404(Account, id=from_acc_id, user=request.user)
        to_account = get_object_or_404(Account, id=to_acc_id, user=request.user)

        if from_account == to_account:
            messages.error(request, "Bir xil hamyonga o'tkazma qilib bo'lmaydi!")
            return redirect('transfer')

        # --- KONVERTATSIYA MANTIQI ---
        
        # 1. Chiquvchi hamyondan qancha ayirishni hisoblash
        if currency == from_account.currency:
            amount_for_from = amount
        elif currency == 'USD' and from_account.currency == 'UZS':
            amount_for_from = (amount * USD_TO_UZS).quantize(Decimal('1'), rounding=ROUND_DOWN)
        elif currency == 'UZS' and from_account.currency == 'USD':
            amount_for_from = (amount / USD_TO_UZS).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        else:
            amount_for_from = amount

        # 2. Kiruvchi hamyonga qancha qo'shishni hisoblash
        if currency == to_account.currency:
            amount_for_to = amount
        elif currency == 'UZS' and to_account.currency == 'USD':
            # So'm o'tkazilsa, Visaga dollarda tushishi uchun
            amount_for_to = (amount / USD_TO_UZS).quantize(Decimal('0.01'), rounding=ROUND_DOWN)
        elif currency == 'USD' and to_account.currency == 'UZS':
            # Dollar o'tkazilsa, Uzcardga so'mda tushishi uchun
            amount_for_to = (amount * USD_TO_UZS).quantize(Decimal('1'), rounding=ROUND_DOWN)
        else:
            amount_for_to = amount

        # 3. Dashboard uchun UZS ekvivalentini aniqlash (MUHIM!)
        # Agar USD o'tkazilsa 12800 ga ko'paytiramiz, aks holda o'zini olamiz
        amount_in_uzs = (amount * USD_TO_UZS).quantize(Decimal('1')) if currency == 'USD' else amount

        # --- TRANZAKSIYANI BAZAGA YOZISH ---
        if from_account.balance < amount_for_from:
            messages.error(request, "Hamyonda mablag' yetarli emas!")
            return redirect('transfer')

        with db_transaction.atomic():
            # Balanslarni yangilash
            from_account.balance -= amount_for_from
            to_account.balance += amount_for_to
            from_account.save()
            to_account.save()
            
            # Tranzaksiya tarixini yaratish
            Transaction.objects.create(
                user=request.user, 
                account=from_account, 
                amount=amount, 
                currency=currency,
                amount_in_uzs=amount_in_uzs, # Dashboard xato qilmasligi uchun shart!
                is_transfer=True, 
                to_account=to_account, 
                comment=f"Transfer: {from_account.name} -> {to_account.name}",
                date=date
            )

        messages.success(request, f"O'tkazma bajarildi: {amount_for_to} {to_account.currency} tushdi.")
        return redirect('dashboard')

# ===================== 4. KATEGORIYA =====================
class CategoryCreateView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'transactions/category_form.html')

    def post(self, request):
        Category.objects.create(
            user=request.user,
            name=request.POST.get('name'),
            kind=request.POST.get('kind'),
            icon=request.POST.get('icon', 'fa-wallet')
        )
        return redirect('dashboard')