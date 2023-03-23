from django.shortcuts import render
import binance
from django.http import JsonResponse


def index(request):
    client = binance.Client()
    # print(client.get_all_tickers())
    # print(client.get_symbol_info('XRPUSDT')['baseAsset'])
    # print(client.get_symbol_info('XRPUSDT')['priceChangePercent'])
    # print(client.get_ticker())
    data_price = [i[1] for i in client.get_klines(symbol='BTCUSDT', interval='1m')][:100]
    data = {'data': data_price}
    min_data = int(min(data['data']).split('.')[0])
    max_data = int(max(data['data']).split('.')[0])
    data_len = []
    for i in reversed(range(len(data_price))):
        data_len.append(str(i+1) + 'm ago')
    data = {'min_data': min_data, 'max_data': max_data, 'data': data['data'][:100], 'data_len': data_len}
    # data = {
    #     'BTC': client.get_symbol_info('BTCUSDT'),
    #     'ETH': client.get_symbol_info('ETHUSDT'),
    #     'BNB': client.get_symbol_info('BNBUSDT'),
    #     'USDT': client.get_symbol_info('USDT'),
    #     'ADA': client.get_symbol_info('ADAUSDT'),
    #     'XRP': client.get_symbol_info('XRPUSDT'),
    #     'DOT': client.get_symbol_info('DOTUSDT'),
    #     'UNI': client.get_symbol_info('UNIUSDT'),
    #     'MATIC': client.get_symbol_info('MATICUSDT'),
    #     'DOGE': client.get_symbol_info('DOGEUSDT'),
    #         }
    if is_ajax(request=request):
        return JsonResponse(data, status=200)
    return render(request, 'index.html')


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
