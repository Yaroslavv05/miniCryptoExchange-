from django import forms


class SearchCoinForm(forms.Form):
    name_coin = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'BTCUSDT',
        'type': 'text'
    }))
    


class BUYForm(forms.Form):
    def __init__(self, *args, **kwargs):
        initial_price = kwargs.pop('initial_price', None)
        super(BUYForm, self).__init__(*args, **kwargs)
        self.fields['price'] = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'text',
            'id': 'buy-price',
            'name': 'buy-price',
            'value': initial_price
        }))
        self.fields['amount'] = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'text',
            'id': 'buy-amount',
            'name': 'buy-amount'
        }))