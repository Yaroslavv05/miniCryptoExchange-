from django.shortcuts import render
import binance
from django.http import JsonResponse

client = binance.Client()


def index(request):
    # print(client.get_all_tickers())
    # print(client.get_symbol_info('XRPUSDT')['baseAsset'])
    # print(client.get_symbol_info('XRPUSDT')['priceChangePercent'])
    data = {
        'BTC': {'price': round(float(client.get_ticker(symbol='BTCUSDT')['lastPrice']), 4),
                'per': round(float(client.get_ticker(symbol='BTCUSDT')['priceChangePercent']) + 2.5, 2)},
        'ETH': {'price': round(float(client.get_ticker(symbol='ETHUSDT')['lastPrice']), 4),
                'per': round(float(client.get_ticker(symbol='ETHUSDT')['priceChangePercent']) + 2.5, 2)},
        'BNB': {'price': round(float(client.get_ticker(symbol='BNBUSDT')['lastPrice']), 4),
                'per': round(float(client.get_ticker(symbol='BNBUSDT')['priceChangePercent']) + 2.5, 2)},
        'ADA': {'price': round(float(client.get_ticker(symbol='ADAUSDT')['lastPrice']), 4),
                'per': round(float(client.get_ticker(symbol='ADAUSDT')['priceChangePercent']) + 2.5, 2)},
        'XRP': {'price': round(float(client.get_ticker(symbol='XRPUSDT')['lastPrice']), 4),
                'per': round(float(client.get_ticker(symbol='XRPUSDT')['priceChangePercent']) + 2.5, 2)},
        'DOT': {'price': round(float(client.get_ticker(symbol='DOTUSDT')['lastPrice']), 4),
                'per': round(float(client.get_ticker(symbol='DOTUSDT')['priceChangePercent']) + 2.5, 2)},
        'UNI': {'price': round(float(client.get_ticker(symbol='UNIUSDT')['lastPrice']), 4),
                'per': round(float(client.get_ticker(symbol='UNIUSDT')['priceChangePercent']) + 2.5, 2)},
        'MATIC': {'price': round(float(client.get_ticker(symbol='MATICUSDT')['lastPrice']), 4),
                  'per': round(float(client.get_ticker(symbol='MATICUSDT')['priceChangePercent']) + 2.5, 2)},
        'DOGE': {'price': round(float(client.get_ticker(symbol='DOGEUSDT')['lastPrice']), 4),
                 'per': round(float(client.get_ticker(symbol='DOGEUSDT')['priceChangePercent']) + 2.5, 2)},
    }
    if is_ajax(request=request):
        return JsonResponse(data, status=200)
    return render(request, 'main/index.html', {'data': data})


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
