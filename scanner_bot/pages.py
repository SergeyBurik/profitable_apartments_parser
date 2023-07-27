from telebot import types
from settings import *
from utils import *
import json


class Controller:
	def __init__(self, bot):
		self.bot = bot
		self.scanner_query_data = {}

	def get_menu(self, msg_id):
		"""
		method that returns menu keyboard
		"""
		keyboard = types.InlineKeyboardMarkup()

		key_start_scanner = types.InlineKeyboardButton(text='Scanner', callback_data=START_SCANNER)
		keyboard.add(key_start_scanner)

		keyboard.add(get_menu_button())

		self.bot.send_message(msg_id, text="Menu", reply_markup=keyboard)

	def handle_dialog(self, call, data):
		"""
		routing dialog data
		"""
		if data["data_type"] == "bedrooms":
			self.bedrooms_number(call, data)

	def bedrooms_number(self, call, data):
		"""
		save bedrooms number to query
		and ask for metro station name
		"""
		self.scanner_query_data[call.message.chat.id]["bedrooms"] = data["data"]
		self.scanner_query_data[call.message.chat.id]["last_bot_message"] = call

		message = self.bot.edit_message_text(
			chat_id=call.message.chat.id,
			message_id=call.message.id,
			text="Enter metro station:",
		)
		self.bot.register_next_step_handler(message, self.metro_station_name)

	def metro_station_name(self, call):
		"""
		save metro station name
		and ask for min square size
		"""
		self.scanner_query_data[call.chat.id]["metro_station"] = check_metro_name(call.text)

		keyboard = types.InlineKeyboardMarkup()

		for i in range(10, 110, 10):
			text = str(i)
			key_bedrooms = types.InlineKeyboardButton(
				text=text,
				callback_data=json.dumps({
					"user": call.chat.id, "data_type": "min_square", "data": text
				})
			)
			keyboard.add(key_bedrooms)

		self.bot.send_message(
			call.chat.id,
			text="Choose minimum square size",
			reply_markup=keyboard
		)

	def start_scanner(self, call):
		"""
		method that starts scanner dialog to fill parser query,
		next question: bedrooms number
		"""
		keyboard = types.InlineKeyboardMarkup()

		for i in range(0, 6):
			text = "Studio" if i == 0 else i
			key_bedrooms = types.InlineKeyboardButton(
				text=text,
				callback_data=json.dumps({
					"user": call.message.chat.id, "data_type": "bedrooms", "data": text
				})
			)
			keyboard.add(key_bedrooms)

		keyboard.add(get_menu_button())

		# create new query object
		self.scanner_query_data[call.message.chat.id] = {}

		self.bot.edit_message_text(
			chat_id=call.message.chat.id,
			message_id=call.message.id,
			text="Choose bedrooms number",
			reply_markup=keyboard
		)
