from django import forms
from .models import Purchase




class CardSearchForm(forms.Form):
    owner_name = forms.CharField(required=False, label='Имя владельца')
    card_number = forms.CharField(required=False, label='Номер карты')
    status = forms.CharField(required=False, label='Статус')

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['seller_name', 'purchase_date', 'purchase_cost']

class PurchaseDeleteForm(forms.Form):
    purchases = forms.ModelMultipleChoiceField(
        queryset=Purchase.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )