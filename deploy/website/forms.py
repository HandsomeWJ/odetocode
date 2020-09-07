from django import forms

class PortfolioForm(forms.Form):
    score = forms.IntegerField(required=True)