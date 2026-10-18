from django import forms
from decimal import Decimal
from apps.market.models import Stock
from .models import Transaction

class TransactionForm(forms.ModelForm):
    stock = forms.ModelChoiceField(
        queryset=Stock.objects.filter(is_active=True).order_by('symbol'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Transaction
        fields = ['stock', 'transaction_type', 'quantity', 'price', 'charges', 'date', 'notes']
        widgets = {
            'transaction_type': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.0001', 'placeholder': 'e.g. 10'}),
            'price': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'placeholder': 'Price per share'}),
            'charges': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01', 'placeholder': '0.00'}),
            'date': forms.DateInput(attrs={'class': 'form-input', 'type': 'date'}),
            'notes': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Order reference, rationale, etc.'}),
        }

    def clean_quantity(self):
        qty = self.cleaned_data.get('quantity')
        if qty is None or qty <= Decimal('0'):
            raise forms.ValidationError("Quantity must be greater than zero.")
        return qty

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None or price <= Decimal('0'):
            raise forms.ValidationError("Price must be greater than zero.")
        return price
