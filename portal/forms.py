from django import forms
from .models import TenantProfile, Bedsitter, Invoice, Apartment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# UserCreationForm already includes 'username', 'password1', 'password2'

class TenantProfileForm(forms.ModelForm):
    class Meta:
        model = TenantProfile
        fields = ['user', 'bedsitter', 'phone']

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ["tenant", 
                  "description", 
                  "amount",
                  "due_date",
                  "is_paid",
                ]
        
class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = ["name", "address"]

class BedsitterForm(forms.ModelForm):
    class Meta:
        model = Bedsitter
        fields = ["apartment", "number"]