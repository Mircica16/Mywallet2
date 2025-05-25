from .models import Expense, Income
from django.db.models import Sum
from django.utils import timezone


def budget_processor(request):
    if request.user.is_authenticated:
        today = timezone.now().date()
        month_start = today.replace(day=1)


        monthly_expenses = Expense.objects.filter(
            user=request.user,
            date__gte=month_start,
            date__lte=today
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        monthly_income = Income.objects.filter(
            user=request.user,
            date__gte=month_start,
            date__lte=today
        ).aggregate(Sum('amount'))['amount__sum'] or 0


        savings = monthly_income - monthly_expenses
        budget = 5000
        budget_remaining = budget - monthly_expenses

        return {
            'total_expenses': monthly_expenses,
            'total_income': monthly_income,
            'total_savings': savings,
            'budget': budget,
            'budget_remaining': budget_remaining
        }
    return {}
