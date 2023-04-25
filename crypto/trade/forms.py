from django import forms


class SearchCoinForm(forms.Form):
    name_coin = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'BTCUSDT',
        'type': 'text',
        'id': 'search-input',
        'style': 'color: white; background: rgb(16, 35, 49);'
    }))


class BUYForm(forms.Form):
    def __init__(self, *args, **kwargs):
        initial_price = kwargs.pop('initial_price', None)
        super(BUYForm, self).__init__(*args, **kwargs)
        self.fields['price'] = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'text',
            'id': 'buy-price',
            'name': 'buy-price',
            'value': initial_price,
            'style': 'background: rgb(16, 35, 49); color: white;'
        }))
        self.fields['amount'] = forms.CharField(widget=forms.TextInput(attrs={
            'type': 'text',
            'id': 'buy-amount',
            'name': 'buy-amount',
            'style': 'background: rgb(16, 35, 49); color: white;'
        }))