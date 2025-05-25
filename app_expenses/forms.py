from django import forms
from .models import Expense, Income, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 3:
            raise forms.ValidationError("Numele categoriei trebuie să aibă cel puțin 3 caractere.")
        return name


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['category', 'amount', 'date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')

        if amount is not None and amount <= 0:
            self.add_error('amount', "Suma trebuie să fie pozitivă.")

        return cleaned_data


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'date', 'description']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get('amount')

        if amount is not None and amount <= 0:
            self.add_error('amount', "Suma trebuie să fie pozitivă.")

        return cleaned_data


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Adresa de email")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Această adresă de email este deja utilizată.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
