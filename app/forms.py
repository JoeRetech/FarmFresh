from django import forms
from .models import FarmerRequest 

class EmailForm(forms.Form):
    requester = forms.ModelChoiceField(
        queryset=FarmerRequest.objects.all(),
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )
