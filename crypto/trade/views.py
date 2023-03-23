from django.shortcuts import render
import binance
from django.http import JsonResponse


def divine_number(number_str: str, length: int = 0) -> str:
    left_side = f'{int(number_str.split(".")[0]):,}'
    if length >= 1:
        right_side = number_str.split(".")[1][:length]
        if right_side[1] == '0':
            right_side = '1'
        return f'{left_side.replace(",", "")}.{right_side}'
    return left_side


def index(request):
    client = binance.Client()
    # print(client.get_all_tickers())
    # print(client.get_symbol_info('XRPUSDT')['baseAsset'])
    # print(client.get_symbol_info('XRPUSDT')['priceChangePercent'])
    # print(client.get_ticker())
    data_price = [i[1] for i in client.get_klines(symbol='ADAUSDT', interval='1m')][:100]
    data = {'data': data_price}
    min_data = divine_number(min(data['data']), 4)
    max_data = divine_number(max(data['data']), 4)
    min_data = str(float(min_data) - (float(min_data) * 0.1 / 100))
    max_data = str(float(max_data) + (float(max_data) * 0.1 / 100))
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
