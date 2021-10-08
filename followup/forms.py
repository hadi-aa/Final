from django import forms
from . import models


class QuoteItemForm(forms.ModelForm):
    class Meta:
        model = models.QuoteItem
        fields = [
            'product',
            'quantity',
            'discount',
        ]
