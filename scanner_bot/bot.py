import json
import os
import telebot
from settings import *
from pages import Controller
from dotenv import load_dotenv

dotenv_path = os.path.join(os.getcwd(), ".env")
load_dotenv(dotenv_path)
BOT_TOKEN = os.environ.get("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)
controller = Controller(bot)


@bot.message_handler(content_types=['text'])
def start(message):
	"""
	function that handles /start action
	"""
	if message.text == '/menu':
		controller.get_menu(message.from_user.id)
	else:
		bot.send_message(message.from_user.id, 'To show menu, type /menu')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
	"""
	function that routes user requests
	"""
	print(call.data)
	if call.data == MENU:
		controller.get_menu(call.message.chat.id)
	elif call.data == START_SCANNER:
		controller.start_scanner(call)
	else:
		try:
			data = json.loads(call.data)
			controller.handle_dialog(call, data)
		except Exception as e:
			print(e)


print("Server started")

bot.polling(none_stop=True, interval=0)
