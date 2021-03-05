import requests
from misc import token
from yobit import get_btc, get_eth
from time import sleep

URL = 'https://api.telegram.org/bot' + token + '/'

global last_update_id
last_update_id = 0


def get_updates():
	url = URL + 'getupdates'
	r = requests.get(url)
	return r.json()


def get_message():
	data = get_updates()
	last_message = data['result'][-1]
	update_id = last_message['update_id']
	chat_id = last_message['message']['chat']['id']
	message_text = last_message['message']['text']
	message = {'update_id': update_id,
				'chat_id': chat_id,
				'text': message_text}
	return message


def send_message(chat_id, text = "Wait a second please..."):
	url = URL + 'sendmessage?chat_id={}&text={}'.format(chat_id, text)
	return requests.get(url)


def main():
	last_update_id = 0

	while True:
		answer = get_message()
		update_id = answer['update_id']
		chat_id = answer['chat_id']
		text = answer['text']

		if last_update_id != update_id and text == '/btc':
			send_message(chat_id, get_btc())
			last_update_id = update_id

		if last_update_id != update_id and text == '/eth':
			send_message(chat_id, get_eth())
			last_update_id = update_id



if __name__ == '__main__':
	main()

















	
