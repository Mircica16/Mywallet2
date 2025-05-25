from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.mail import EmailMessage
from django.conf import settings

from .forms import ExpenseForm, IncomeForm, CategoryForm, CustomUserCreationForm
from .models import Expense, Income, Category



class ExpenseListView(LoginRequiredMixin, ListView):
    model = Expense
    template_name = 'expenses/expense_list.html'
    context_object_name = 'expenses'

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user).order_by('-date')


class ExpenseDetailView(LoginRequiredMixin, DetailView):
    model = Expense
    template_name = 'expenses/expense_detail.html'
    context_object_name = 'expense'

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)


class ExpenseCreateView(LoginRequiredMixin, CreateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expense-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['category'].queryset = Category.objects.filter(user=self.request.user)
        return form


class ExpenseUpdateView(LoginRequiredMixin, UpdateView):
    model = Expense
    form_class = ExpenseForm
    template_name = 'expenses/expense_form.html'
    success_url = reverse_lazy('expense-list')

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['category'].queryset = Category.objects.filter(user=self.request.user)
        return form


class ExpenseDeleteView(LoginRequiredMixin, DeleteView):
    model = Expense
    template_name = 'expenses/expense_confirm_delete.html'
    success_url = reverse_lazy('expense-list')

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)




class IncomeListView(LoginRequiredMixin, ListView):
    model = Income
    template_name = 'income/income_list.html'
    context_object_name = 'incomes'

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user).order_by('-date')


class IncomeDetailView(LoginRequiredMixin, DetailView):
    model = Income
    template_name = 'income/income_detail.html'
    context_object_name = 'income'

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)


class IncomeCreateView(LoginRequiredMixin, CreateView):
    model = Income
    form_class = IncomeForm
    template_name = 'income/income_form.html'
    success_url = reverse_lazy('income-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class IncomeUpdateView(LoginRequiredMixin, UpdateView):
    model = Income
    form_class = IncomeForm
    template_name = 'income/income_form.html'
    success_url = reverse_lazy('income-list')

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)


class IncomeDeleteView(LoginRequiredMixin, DeleteView):
    model = Income
    template_name = 'income/income_confirm_delete.html'
    success_url = reverse_lazy('income-list')

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user)




class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'category/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/category_form.html'
    success_url = reverse_lazy('category-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/category_form.html'
    success_url = reverse_lazy('category-list')

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)


class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'category/category_confirm_delete.html'
    success_url = reverse_lazy('category-list')

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)




@login_required
def dashboard(request):
    today = timezone.now().date()
    range_filter = request.GET.get('range', 'month')  # default: luna

    if range_filter == 'week':
        start_date = today - timezone.timedelta(days=7)
    elif range_filter == 'year':
        start_date = today.replace(month=1, day=1)
    else:  # default 'month'
        start_date = today.replace(day=1)

    month_start = today.replace(day=1)

    monthly_expenses = Expense.objects.filter(user=request.user, date__gte=start_date, date__lte=today)
    monthly_income = Income.objects.filter(user=request.user, date__gte=start_date, date__lte=today)

    total_expenses = monthly_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    total_income = monthly_income.aggregate(Sum('amount'))['amount__sum'] or 0

    savings_expenses = monthly_expenses.filter(category__name__icontains='economii')
    savings = savings_expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    budget = Income.objects.filter(
        user=request.user,
        date__gte= month_start,
        date__lte=today
    ).aggregate(Sum('amount'))['amount__sum'] or 0
    budget_remaining = budget - total_expenses

    expense_categories = monthly_expenses.values('category__name').annotate(total=Sum('amount')).order_by('-total')

    recent_expenses = Expense.objects.filter(user=request.user).order_by('-date')[:5]
    recent_incomes = Income.objects.filter(user=request.user).order_by('-date')[:5]

    recent_transactions = [
        {'type': 'expense', 'amount': e.amount, 'date': e.date, 'description': e.description, 'category': e.category.name if e.category else 'No Category'}
        for e in recent_expenses
    ] + [
        {'type': 'income', 'amount': i.amount, 'date': i.date, 'description': i.description}
        for i in recent_incomes
    ]

    recent_transactions.sort(key=lambda x: x['date'], reverse=True)
    recent_transactions = recent_transactions[:5]

    context = {
        'monthly_expenses': total_expenses,
        'monthly_income': total_income,
        'savings': savings,
        'expense_categories': expense_categories,
        'recent_transactions': recent_transactions,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'total_savings': savings,
        'budget': budget,
        'budget_remaining': budget_remaining,
        'range_filter': range_filter,
    }
    return render(request, 'expenses/dashboard.html', context)



@login_required
def send_monthly_report(request):
    today = timezone.now().date()
    month_start = today.replace(day=1)

    monthly_expenses = Expense.objects.filter(user=request.user, date__gte=month_start, date__lte=today)
    monthly_income = Income.objects.filter(user=request.user, date__gte=month_start, date__lte=today)

    total_expenses = monthly_expenses.aggregate(Sum('amount'))['amount__sum'] or 0
    total_income = monthly_income.aggregate(Sum('amount'))['amount__sum'] or 0
    savings = total_income - total_expenses

    expense_categories = monthly_expenses.values('category__name').annotate(total=Sum('amount')).order_by('-total')

    subject = f"Raport Cheltuieli Lunare - {today.strftime('%B %Y')}"
    lines = [
        f"Buna {request.user.username},",
        "",
        f"Raportul tau lunar pentru {today.strftime('%B %Y')}:",
        f"- Venituri totale: {total_income:.2f} RON",
        f"- Cheltuieli totale: {total_expenses:.2f} RON",
        f"- Economii: {savings:.2f} RON",
        "",
        "Cheltuieli pe categorii:"
    ]
    for cat in expense_categories:
        nume = cat['category__name'] or 'Fara Categorie'
        suma = cat['total']
        lines.append(f"- {nume}: {suma:.2f} RON")

    message = "\n".join(lines)

    try:
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[request.user.email],
        )
        email.content_subtype = 'plain'
        email.encoding = 'utf-8'
        email.send(fail_silently=False)
    except Exception as e:
        print("Eroare la trimiterea emailului:", e)

    return redirect('dashboard')



def register_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})
