import random

from django.shortcuts import render, redirect
import binance
from django.http import JsonResponse
from django.contrib import messages
from .forms import SearchCoinForm, BUYForm


def divine_number(number_str: str, length: int = 0) -> str:
    left_side = f'{int(number_str.split(".")[0]):,}'
    if length >= 1:
        try:
            right_side = number_str.split(".")[1][:length]
        except IndexError:
            return left_side
        if right_side[1] == '0':
            right_side = '1'
        return f'{left_side.replace(",", "")}.{right_side}'
    return left_side


def get_price_change(request):
    client = binance.Client()
    try:
        is_first = True if request.COOKIES['is_first'] == 'True' else False
    except KeyError:
        is_first = False
    try:
        name = request.COOKIES['name']
    except KeyError:
        name = 'BTCUSDT'
    if not is_first:
        data_price = [i[4] for i in client.get_klines(symbol=name, interval='1m')][:100]
        info = client.get_ticker(symbol=name)
        data = {
            'price': divine_number(data_price[-1], 4),
            'change': round(float(info['priceChangePercent']), 2),
        }
    else:
        data_price = [i[4] for i in client.get_klines(symbol='BTCUSDT', interval='1m')][:100]
        info = client.get_ticker(symbol='BTCUSDT')
        data = {
            'price': divine_number(data_price[-1], 4),
            'change': round(float(info['priceChangePercent']), 2),
        }
    return JsonResponse(data)


def spot(request):
    name = 'BTCUSDT'
    client = binance.Client()
    if request.method == 'POST':
        form = SearchCoinForm(request.POST)
        if form.is_valid():
            name_coin = form.cleaned_data['name_coin']
            response = redirect('spot_coin')
            response.set_cookie('name', name_coin)
            response.set_cookie('is_first', False)
            return response
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = SearchCoinForm()
    if request.method == 'POST':
        buy_form = BUYForm(request.POST)
        if buy_form.is_valid():
            price = buy_form.cleaned_data['price']
            amount = buy_form.cleaned_data['amount']
            response = redirect('pay')
            response.set_cookie('price', price)
            response.set_cookie('amount', amount)
            return response
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        data_price = [i[4] for i in client.get_klines(symbol=name, interval='1m')][:100]
        info = client.get_ticker(symbol=name)
        buy_form = BUYForm(initial_price=float(data_price[-1]))
    info = client.get_ticker(symbol=name)
    data_price = [i[4] for i in client.get_klines(symbol=name, interval='1m')][:100]
    # print(client.get_klines(symbol=name, interval='1m'))
    data = {'data': data_price}
    min_data = divine_number(min(data['data']), 4)
    max_data = divine_number(max(data['data']), 4)
    min_data = str(float(min_data) - (float(min_data) * 0.1 / 100))
    max_data = str(float(max_data) + (float(max_data) * 0.1 / 100))
    data_len = []
    asset = client.get_symbol_info(symbol=name)
    for i in reversed(range(len(data_price))):
        data_len.append(str(i + 1) + 'm ago')
    data = {'min_data': min_data, 'max_data': max_data, 'data': data['data'], 'data_len': data_len}
    if is_ajax(request=request):
        return JsonResponse(data, status=200)
    return render(request, 'index.html',
                  {'form': form, 'symbol': info['symbol'], 'price': divine_number(data_price[-1], 4),
                   'change': round(float(info['priceChangePercent']), 2), 'asset': asset['baseAsset'],
                   'currency': asset['quoteAsset'], 'buy_form': buy_form, 'price2': float(data_price[-1])})


def spot_coin(request):
    client = binance.Client()
    if request.method == 'POST':
        form = SearchCoinForm(request.POST)
        if form.is_valid():
            name_coin = form.cleaned_data['name_coin']
            response = redirect('spot_coin')
            response.set_cookie('name', name_coin)
            response.set_cookie('is_first', False)
            return response
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        form = SearchCoinForm()
    if request.method == 'POST':
        buy_form = BUYForm(request.POST)
        if buy_form.is_valid():
            price = buy_form.cleaned_data['price']
            amount = buy_form.cleaned_data['amount']
            response = redirect('pay')
            response.set_cookie('price', price)
            response.set_cookie('amount', amount)
            return response
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)
    else:
        data_price = [i[1] for i in client.get_klines(symbol=request.COOKIES['name'], interval='1m')][:100]
        buy_form = BUYForm(initial_price=float(data_price[-1]))
    data_price = [i[1] for i in client.get_klines(symbol=request.COOKIES['name'], interval='1m')][:100]
    data = {'data': data_price}
    min_data = divine_number(min(data['data']), 4)
    max_data = divine_number(max(data['data']), 4)
    min_data = str(float(min_data) - (float(min_data) * 0.1 / 100))
    max_data = str(float(max_data) + (float(max_data) * 0.1 / 100))
    data_len = []
    info = client.get_ticker(symbol=request.COOKIES['name'])
    asset = client.get_symbol_info(symbol=request.COOKIES['name'])
    for i in reversed(range(len(data_price))):
        data_len.append(str(i + 1) + 'm ago')
    data = {'min_data': min_data, 'max_data': max_data, 'data': data['data'][:100], 'data_len': data_len}
    if is_ajax(request=request):
        return JsonResponse(data, status=200)
    return render(request, 'index.html',
                  {'form': form, 'symbol': info['symbol'], 'price': divine_number(data_price[-1], 4),
                   'change': round(float(info['priceChangePercent']), 2), 'asset': asset['baseAsset'],
                   'currency': asset['quoteAsset'], 'buy_form': buy_form, 'price2': float(data_price[-1])})


def pay(request):
    name_coin = request.COOKIES['name']
    price = request.COOKIES['price']
    amount = request.COOKIES['amount']
    suuma = float(price) * float(amount)
    client = binance.Client()
    info = client.get_ticker(symbol=request.COOKIES['name'])
    asset = client.get_symbol_info(symbol=request.COOKIES['name'])
    return render(request, 'Pay.html', {'name_coin': name_coin, 'price': price, 'amount': amount, 'summa': suuma, 'asset': asset['baseAsset'], 'currency': asset['quoteAsset']})


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
