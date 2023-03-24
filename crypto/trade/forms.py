from django import forms


class SearchCoinForm(forms.Form):
    name_coin = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'BTCUSDT',
        'type': 'text'
    }))


class BUYForm(forms.Form):
    price = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'id': 'buy-price',
        'name': 'buy-price'
    }))
    amount = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'text',
        'id': 'buy-amount',
        'name': 'buy-amount'
    }))