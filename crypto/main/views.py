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


def chart(request):
    data_price = [i[1] for i in client.get_klines(symbol='BTCUSDT', interval='1m')][:100]
    data = {'data': data_price}
    min_data = int(min(data['data']).split('.')[0])
    max_data = int(max(data['data']).split('.')[0])
    data_len = []
    for i in reversed(range(len(data_price))):
        data_len.append(str(i + 1) + 'm ago')
    data = {'min_data': min_data, 'max_data': max_data, 'data': data['data'][:100], 'data_len': data_len}
    if is_ajax(request=request):
        return JsonResponse(data, status=200)
    return render(request, 'main/chart.html')


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'