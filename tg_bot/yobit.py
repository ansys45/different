import urllib.request
import requests
import json

def get_btc():
	urlB = 'https://yobit.net/api/2/btc_usd/ticker'
	resp = requests.get(urlB).json()
	price = resp['ticker']['last']
	return str(price) + ' usd'

def get_eth():
	urlB = 'https://yobit.net/api/2/eth_usd/ticker'
	resp = requests.get(urlB).json()
	price = resp['ticker']['last']
	return str(price) + ' usd'

# print(get_btc())
