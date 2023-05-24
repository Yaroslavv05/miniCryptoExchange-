from django.shortcuts import render, redirect
import binance
from django.http import JsonResponse
from django.contrib import messages
from .forms import SearchCoinForm, BUYForm
from .config import INFO
from web3 import Web3
import asyncio
from asgiref.sync import async_to_sync
import aiohttp


def divine_number(number_str: str, length: int = 0) -> str:
    left_side = f'{int(number_str.split(".")[0]):,}'
    if length >= 1:
        try:
            right_side = number_str.split(".")[1][:length]
        except IndexError:
            return left_side
        try:
            if right_side[1] == '0':
                right_side = '1'
        except IndexError:
            pass
        return f'{left_side.replace(",", "")}.{right_side}'
    return left_side


def get_price_change(request):
    client = binance.Client()
    try:
        is_first = True if request.COOKIES['is_first'] == 'True' else False
    except KeyError:
        is_first = True
    try:
        name = request.COOKIES['name']
    except KeyError:
        name = 'BTCUSDT'
    if not is_first:
        data_price = [i[4] for i in client.get_klines(symbol=name, interval='1m')][:100]
        data_price = [str(float(i) + (float(i) * 0.03)) for i in data_price]
        info = client.get_ticker(symbol=name)
        data = {
            'price': divine_number(data_price[-1], 4),
            'change': round(float(info['priceChangePercent']), 2),
        }
    else:
        data_price = [i[4] for i in client.get_klines(symbol='BTCUSDT', interval='1m')][:100]
        data_price = [str(float(i) + (float(i) * 0.03)) for i in data_price]
        info = client.get_ticker(symbol='BTCUSDT')
        data = {
            'price': divine_number(data_price[-1], 4),
            'change': round(float(info['priceChangePercent']), 2),
        }
    return JsonResponse(data)


async def fetch_ticker(session, symbol):
    async with session.get(f'https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}') as response:
        ticker = await response.json()
        return {
            'name': symbol,
            'price': round(float(ticker['lastPrice']) * 1.03, 4),
            'change': round(float(ticker['priceChangePercent']), 2)
        }


def spot(request):
    name = 'BTCUSDT'
    client = binance.Client()

    # Получение данных о ценах
    klines = client.get_klines(symbol=name, interval='1m')
    data_price = [str((float(i[4]) * 1.03)) for i in klines[:100]]

    if request.method == 'POST':
        form = SearchCoinForm(request.POST)
        if form.is_valid():
            name_coin = form.cleaned_data['name_coin'].upper()
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
            for error in list(buy_form.errors.values()):
                messages.error(request, error)
    else:
        buy_form = BUYForm(initial_price=round(float(data_price[-1]), 4))

    info = client.get_ticker(symbol=name)
    data_len = [str(i + 1) + 'm ago' for i in reversed(range(len(data_price)))]

    # Подготовка данных для передачи в шаблон
    data = {
        'min_data': str(float(min(data_price)) - (float(min(data_price)) * 0.1 / 100)),
        'max_data': str(float(max(data_price)) + (float(max(data_price)) * 0.1 / 100)),
        'data': data_price,
        'data_len': data_len
    }

    if is_ajax(request=request):
        return JsonResponse(data, status=200)

    async def get_ticker_info():
        async with aiohttp.ClientSession() as session:
            symbols = [symbol + 'USDT' for symbol in INFO.keys()]
            tasks = []
            for symbol in symbols:
                tasks.append(fetch_ticker(session, symbol))

            return await asyncio.gather(*tasks)

    infos = async_to_sync(get_ticker_info)()

    asset = client.get_symbol_info(symbol='BTCUSDT')
    response = render(request, 'index.html', {
        'form': form,
        'symbol': info['symbol'],
        'price': divine_number(data_price[-1], 4),
        'change': round(float(info['priceChangePercent']), 2),
        'asset': asset['baseAsset'],
        'currency': asset['quoteAsset'],
        'buy_form': buy_form,
        'price2': round(float(data_price[-1]), 4),
        'name_coins': list(INFO.keys()),
        'infos': infos
    })

    response.set_cookie('name', 'BTCUSDT')
    return response


def spot_coin(request):
    client = binance.Client()

    # Получение данных о ценах
    klines = client.get_klines(symbol=request.COOKIES['name'], interval='1m')
    data_price = [str((float(i[4]) * 1.03)) for i in klines[:100]]

    if request.method == 'POST':
        form = SearchCoinForm(request.POST)
        if form.is_valid():
            name_coin = form.cleaned_data['name_coin'].upper()
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
            for error in list(buy_form.errors.values()):
                messages.error(request, error)
    else:
        buy_form = BUYForm(initial_price=round(float(data_price[-1]), 4))

    info = client.get_ticker(symbol=request.COOKIES['name'])
    data_len = [str(i + 1) + 'm ago' for i in reversed(range(len(data_price)))]

    # Подготовка данных для передачи в шаблон
    data = {
        'min_data': str(float(min(data_price)) - (float(min(data_price)) * 0.1 / 100)),
        'max_data': str(float(max(data_price)) + (float(max(data_price)) * 0.1 / 100)),
        'data': data_price,
        'data_len': data_len
    }

    if is_ajax(request=request):
        return JsonResponse(data, status=200)

    async def get_ticker_info():
        async with aiohttp.ClientSession() as session:
            symbols = [symbol + 'USDT' for symbol in INFO.keys()]
            tasks = []
            for symbol in symbols:
                tasks.append(fetch_ticker(session, symbol))

            return await asyncio.gather(*tasks)

    infos = async_to_sync(get_ticker_info)()
    asset = client.get_symbol_info(symbol=request.COOKIES['name'])
    response = render(request, 'index.html', {
        'form': form,
        'symbol': info['symbol'],
        'price': divine_number(data_price[-1], 4),
        'change': round(float(info['priceChangePercent']), 2),
        'asset': asset['baseAsset'],
        'currency': asset['quoteAsset'],
        'buy_form': buy_form,
        'price2': round(float(data_price[-1]), 4),
        'name_coins': list(INFO.keys()),
        'infos': infos
    })
    response.set_cookie('name', request.COOKIES['name'])
    return response


def pay(request):
    name_coin = request.COOKIES['name']
    price = request.COOKIES['price']
    amount = request.COOKIES['amount']
    suuma = float(price) * float(amount)
    client = binance.Client()
    info = client.get_ticker(symbol=request.COOKIES['name'])
    asset = client.get_symbol_info(symbol=request.COOKIES['name'])
    if asset['baseAsset'] in INFO:
        return render(request, 'Pay.html', {'name_coin': name_coin, 'price': price, 'amount': amount, 'summa': suuma,
                                            'asset': asset['baseAsset'], 'currency': asset['quoteAsset'],
                                            'number_wallet': INFO[asset['baseAsset']]['wallet']})
    else:
        return render(request, 'Pay.html', {'name_coin': name_coin, 'price': price, 'amount': amount, 'summa': suuma,
                                            'asset': asset['baseAsset'], 'currency': asset['quoteAsset'],
                                            'number_wallet': 'GGWP'})


def paid(request):
    price = request.COOKIES['price']
    amount = request.COOKIES['amount']
    suuma = float(price) * float(amount)
    client = binance.Client()
    asset = client.get_symbol_info(symbol=request.COOKIES['name'])
    web3 = Web3(Web3.HTTPProvider(INFO[asset['baseAsset']]['api']))
    balance = web3.eth.get_balance(INFO[asset['baseAsset']]['wallet'])
    if balance == (float(balance) + suuma):
        redirect('account_kyc')
    return render(request, 'Paid.html')


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
