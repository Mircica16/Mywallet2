from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import register_view
from .views import send_monthly_report

urlpatterns = [

    path('', views.dashboard, name='dashboard'),
    path('register/', register_view, name='register'),
    path('expenses/', views.ExpenseListView.as_view(), name='expense-list'),
    path('expenses/<int:pk>/', views.ExpenseDetailView.as_view(), name='expense-detail'),
    path('expenses/add/', views.ExpenseCreateView.as_view(), name='expense-create'),
    path('expenses/<int:pk>/edit/', views.ExpenseUpdateView.as_view(), name='expense-update'),
    path('expenses/<int:pk>/delete/', views.ExpenseDeleteView.as_view(), name='expense-delete'),

    path('incomes/', views.IncomeListView.as_view(), name='income-list'),
    path('incomes/<int:pk>/', views.IncomeDetailView.as_view(), name='income-detail'),
    path('incomes/add/', views.IncomeCreateView.as_view(), name='income-create'),
    path('incomes/<int:pk>/edit/', views.IncomeUpdateView.as_view(), name='income-update'),
    path('incomes/<int:pk>/delete/', views.IncomeDeleteView.as_view(), name='income-delete'),

    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/add/', views.CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),

    path('send-monthly-report/', views.send_monthly_report, name='send-monthly-report'),

    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('send-monthly-report/', send_monthly_report, name='send-monthly-report'),
]
