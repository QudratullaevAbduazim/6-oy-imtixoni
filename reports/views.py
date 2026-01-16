from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Sum, Case, When, F, DecimalField
from decimal import Decimal
from datetime import timedelta
from transactions.models import Transaction

class ReportsView(LoginRequiredMixin, View):
    def get(self, request):
        now = timezone.now()
        period = request.GET.get('period', 'month')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        queryset = Transaction.objects.filter(user=request.user)

        if start_date and end_date:
            queryset = queryset.filter(date__date__range=[start_date, end_date])
            period = 'custom'
        elif start_date:
            queryset = queryset.filter(date__date=start_date)
            period = 'custom'
        else:
            if period == 'day':
                queryset = queryset.filter(date__date=now.date())
            elif period == 'week':
                queryset = queryset.filter(date__gte=now - timedelta(days=7))
            else:  
                queryset = queryset.filter(date__gte=now - timedelta(days=30))

        stats = queryset.aggregate(
            total_income=Sum(
                Case(
                    When(category__kind='in', then=F('amount_in_uzs')),
                    default=Decimal('0'),
                    output_field=DecimalField()
                )
            ),
            total_expense=Sum(
                Case(
                    When(category__kind='out', then=F('amount_in_uzs')),
                    default=Decimal('0'),
                    output_field=DecimalField()
                )
            )
        )

        income = stats['total_income'] or Decimal('0')
        expense = stats['total_expense'] or Decimal('0')

        category_data = queryset.filter(category__kind='out').values(
            'category__name'
        ).annotate(
            total=Sum('amount_in_uzs')
        ).order_by('-total')

        current_lang = request.session.get('_language', 'uz')

        context = {
            'transactions': queryset.order_by('-date'),
            'income': income,
            'expense': expense,
            'balance': income - expense,
            'period': period,
            'start_date': start_date,
            'end_date': end_date,
            'category_data': category_data,
            'LANGUAGE_CODE': current_lang
        }
        return render(request, 'reports/reports.html', context)