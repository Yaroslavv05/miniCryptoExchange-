from django.shortcuts import render
import binance
from django.http import JsonResponse

client = binance.Client()


def index(request):
    # print(client.get_all_tickers())
    # print(client.get_symbol_info('XRPUSDT')['baseAsset'])
    # print(client.get_symbol_info('XRPUSDT')['priceChangePercent'])
    # print(client.get_ticker())
    data = {
        'BTC': client.get_ticker(symbol='BTCUSDT'),
        'ETH': client.get_ticker(symbol='ETHUSDT'),
        'BNB': client.get_ticker(symbol='BNBUSDT'),
        # 'USDT': client.get_ticker(symbol='USDT'),
        'ADA': client.get_ticker(symbol='ADAUSDT'),
        'XRP': client.get_ticker(symbol='XRPUSDT'),
        'DOT': client.get_ticker(symbol='DOTUSDT'),
        'UNI': client.get_ticker(symbol='UNIUSDT'),
        'MATIC': client.get_ticker(symbol='MATICUSDT'),
        'DOGE': client.get_ticker(symbol='DOGEUSDT'),
            }
    # print(client.get_ticker(symbol='BTCUSDT'))
    return render(request, 'main/index.html', {'data': data})


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'