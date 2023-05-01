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
                'per': round(float(client.get_ticker(symbol='BTCUSDT')['priceChangePercent']) + 2.5, 2),
                'highPrice': round(float(client.get_ticker(symbol='BTCUSDT')['highPrice']), 4),
                'lowPrice': round(float(client.get_ticker(symbol='BTCUSDT')['lowPrice']), 4),
                'volume': float(client.get_ticker(symbol='BTCUSDT')['volume'])},
        'ETH': {'price': round(float(client.get_ticker(symbol='ETHUSDT')['lastPrice']), 4),
                'per': round(float(client.get_ticker(symbol='ETHUSDT')['priceChangePercent']) + 2.5, 2),
                'highPrice': round(float(client.get_ticker(symbol='ETHUSDT')['highPrice']), 4),
                'lowPrice': round(float(client.get_ticker(symbol='ETHUSDT')['lowPrice']), 4),
                'volume': float(client.get_ticker(symbol='ETHUSDT')['volume'])},
        'BNB': {'price': round(float(client.get_ticker(symbol='BNBUSDT')['lastPrice']), 4),
                'per': round(float(client.get_ticker(symbol='BNBUSDT')['priceChangePercent']) + 2.5, 2),
                'highPrice': round(float(client.get_ticker(symbol='BNBUSDT')['highPrice']), 4),
                'lowPrice': round(float(client.get_ticker(symbol='BNBUSDT')['lowPrice']), 4),
                'volume': float(client.get_ticker(symbol='BNBUSDT')['volume'])},
        'ADA': {'price': round(float(client.get_ticker(symbol='ADAUSDT')['lastPrice']), 4),
                'per': round(float(client.get_ticker(symbol='ADAUSDT')['priceChangePercent']) + 2.5, 2),
                'highPrice': round(float(client.get_ticker(symbol='ADAUSDT')['highPrice']), 4),
                'lowPrice': round(float(client.get_ticker(symbol='ADAUSDT')['lowPrice']), 4),
                'volume': float(client.get_ticker(symbol='ADAUSDT')['volume'])},
        'XRP': {'price': round(float(client.get_ticker(symbol='XRPUSDT')['lastPrice']), 4),
                'per': round(float(client.get_ticker(symbol='XRPUSDT')['priceChangePercent']) + 2.5, 2),
                'highPrice': round(float(client.get_ticker(symbol='XRPUSDT')['highPrice']), 4),
                'lowPrice': round(float(client.get_ticker(symbol='XRPUSDT')['lowPrice']), 4),
                'volume': float(client.get_ticker(symbol='XRPUSDT')['volume'])},
        'DOT': {'price': round(float(client.get_ticker(symbol='DOTUSDT')['lastPrice']), 4),
                'per': round(float(client.get_ticker(symbol='DOTUSDT')['priceChangePercent']) + 2.5, 2),
                'highPrice': round(float(client.get_ticker(symbol='DOTUSDT')['highPrice']), 4),
                'lowPrice': round(float(client.get_ticker(symbol='DOTUSDT')['lowPrice']), 4),
                'volume': float(client.get_ticker(symbol='DOTUSDT')['volume'])},
        'UNI': {'price': round(float(client.get_ticker(symbol='UNIUSDT')['lastPrice']), 4),
                'per': round(float(client.get_ticker(symbol='UNIUSDT')['priceChangePercent']) + 2.5, 2),
                'highPrice': round(float(client.get_ticker(symbol='UNIUSDT')['highPrice']), 4),
                'lowPrice': round(float(client.get_ticker(symbol='UNIUSDT')['lowPrice']), 4),
                'volume': float(client.get_ticker(symbol='UNIUSDT')['volume'])},
        'MATIC': {'price': round(float(client.get_ticker(symbol='MATICUSDT')['lastPrice']), 4),
                  'per': round(float(client.get_ticker(symbol='MATICUSDT')['priceChangePercent']) + 2.5, 2),
                  'highPrice': round(float(client.get_ticker(symbol='MATICUSDT')['highPrice']), 4),
                    'lowPrice': round(float(client.get_ticker(symbol='MATICUSDT')['lowPrice']), 4),
                    'volume': float(client.get_ticker(symbol='MATICUSDT')['volume'])},
        'DOGE': {'price': round(float(client.get_ticker(symbol='DOGEUSDT')['lastPrice']), 4),
                 'per': round(float(client.get_ticker(symbol='DOGEUSDT')['priceChangePercent']) + 2.5, 2),
                 'highPrice': round(float(client.get_ticker(symbol='DOGEUSDT')['highPrice']), 4),
                'lowPrice': round(float(client.get_ticker(symbol='DOGEUSDT')['lowPrice']), 4),
                'volume': float(client.get_ticker(symbol='DOGEUSDT')['volume'])},
    }
    if is_ajax(request=request):
        return JsonResponse(data, status=200)
    return render(request, 'main/Bitfinex.html', {'data': data})


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
