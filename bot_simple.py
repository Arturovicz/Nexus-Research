import time
import requests
import urllib.parse
import hashlib
import hmac
import base64
import decimal

with open('keys', 'r') as f:
    lines = f.read().splitlines()
    api_key = lines[0]
    api_secu = lines[1]
    api_url = lines[2]

buy_limit = 19700
sell_limit = 19800
buy_amount = 0.01
sell_amount = 0.01


def get_kraken_signature(urlpath, data, secret):
    postdata = urllib.parse.urlencode(data)
    encoded = (str(data['nonce']) + postdata).encode()
    message = urlpath.encode() + hashlib.sha256(encoded).digest()

    mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
    sigdigest = base64.b64encode(mac.digest())
    return sigdigest.decode()


def kraken_request(url_path, data, api_key, api_secu):
    headers = {"API-Key": api_key, "API-Sign": get_kraken_signature(url_path, data, api_secu)}
    resp = requests.post((api_url + url_path), headers=headers, data = data)
    return resp


while True:
    current_price = requests.get("https://api.kraken.com/0/public/Ticker?pair=BTCEUR").json()['result']['XXBTZEUR']['c'][0]
    if float(current_price) < buy_limit:
        print(f'Buying {buy_amount} of BTC at {current_price}')
        resp_buy = kraken_request("/0/private/AddOrder", {
            'nonce': str(int(1000 * time.time())),
            'ordertype': 'market',
            'type': 'buy',
            'volume': buy_amount,
            'pair': 'XBTUSD',
            'price': 27000
        }, api_key, api_secu)

        if not resp_buy.json()['error']:
            print('Success')
        else:
            print(f"Error: {resp_buy.json()['error']}")
    elif float(current_price) > sell_limit:
        print(f'Selling {sell_amount} of BTC at {current_price}')
        resp_buy = kraken_request("/0/private/AddOrder", {
            'nonce': str(int(1000 * time.time())),
            'ordertype': 'market',
            'type': 'sell',
            'volume': sell_amount,
            'pair': 'XBTUSD',
            'price': 27000
        }, api_key, api_secu)

        if not resp_buy.json()['error']:
            print('Success')
        else:
            print(f"Error: {resp_buy.json()['error']}")
    else:
        print(f'Current Price: {current_price}, no buy/sell actions available')
    time.sleep(3)