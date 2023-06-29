from django import forms
from django.core import validators

class ProductForm(forms.Form):
    name = forms.CharField(max_length= 30)
    price = forms.DecimalField(min_value= 10, max_value= 30000, decimal_places=2)
    description = forms.CharField(
        label='Product description',
        widget=forms.Textarea(attrs={"rows" : 7, 'cols':15}),
        validators=[validators.RegexValidator(
            regex='great',
            message="Field must contain word 'great'",
        )],
    )