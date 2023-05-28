from django.shortcuts import render
import binance
from django.http import JsonResponse

client = binance.Client()


def index(request):
    symbols = ['BTC', 'ETH', 'BNB', 'ADA', 'XRP', 'DOT', 'UNI', 'MATIC', 'DOGE']
    data = {}

    for symbol in symbols:
        ticker = client.get_ticker(symbol=f'{symbol}USDT')
        price = round(float(ticker['lastPrice']) * 1.03, 4)
        price_change_percent = round(float(ticker['priceChangePercent']) + 2.5, 2)
        high_price = round(float(ticker['highPrice']), 4)
        low_price = round(float(ticker['lowPrice']), 4)
        volume = float(ticker['volume'])

        data[symbol] = {
            'price': price,
            'per': price_change_percent,
            'highPrice': high_price,
            'lowPrice': low_price,
            'volume': volume
        }

    return render(request, 'main/Bitfinex.html', {'data': data})


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
