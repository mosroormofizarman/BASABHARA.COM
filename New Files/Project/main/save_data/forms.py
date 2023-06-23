from django import forms

class MyForm(forms.Form):
    AdsName = forms.CharField(max_length=100)