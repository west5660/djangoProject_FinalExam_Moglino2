# ваше_приложение/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Order


class RegistrationForm(UserCreationForm):
    organization_name = forms.CharField(max_length=255, required=True)
    production_type = forms.CharField(max_length=255, required=True)
    project_status = forms.CharField(max_length=255, required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(max_length=255, required=True, help_text='Enter a valid email address.')

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Пользователь с таким адресом электронной почты уже зарегистрирован.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
            user_profile = UserProfile.objects.create(user=user, organization_name=self.cleaned_data['organization_name'],
                                       production_type=self.cleaned_data['production_type'],
                                       project_status=self.cleaned_data['project_status'],
                                       phone_number=self.cleaned_data['phone_number'],
                                       email=self.cleaned_data['email'])  # Сохраняем электронную почту и имя организации в UserProfile
        return user

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['quantity']
        labels = {'quantity': 'Количество'}

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity <= 0:
            raise forms.ValidationError("Количество должно быть положительным числом.")
        return quantity

class AddToCartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1, widget=forms.NumberInput(attrs={'class': 'quantity-input'}))


from hcaptcha.fields import hCaptchaField



