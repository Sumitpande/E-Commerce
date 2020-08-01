from .models import *
from django.forms import ModelForm

from django import forms


class BidsForm(ModelForm):
    bidding = forms.IntegerField( widget=forms.TextInput(attrs={'placeholder': '$'}))
    
    class Meta:
        model= Bids
        fields = ['bidding', 'buyer_id', 'blisting_id']
    