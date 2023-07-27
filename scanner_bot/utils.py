from telebot import types
from settings import *
import json


def get_menu_button():
	return types.InlineKeyboardButton(text='Меню', callback_data=MENU, n_cols=1)


metro_file = open("C:/Python/ml_aprartments_bot/files/metro_stations.json", encoding="utf-8")
metro = json.load(metro_file)


def check_metro_name(name):
	name = name.lower()
	possible_station = possible_station_line = None
	mncount = 10 ** 2
	for line in metro:
		for station in line["stations"]:
			station_name = station["name"].lower()

			# two pointers method to compare differences between
			# user input and possible station name
			p1 = p2 = 0
			difference_count = 0
			while p1 < len(name) and p2 < len(station_name):
				if name[p1] == station_name[p2]:
					p1 += 1
					p2 += 1
				else:
					if len(name) < len(station_name):
						p2 += 1
					else:
						p1 += 1
					difference_count += 1

			if difference_count <= mncount:
				mncount = difference_count
				possible_station = station
				possible_station_line = line["line"]
			if difference_count == 0:
				return [possible_station, possible_station_line]
	return [possible_station, possible_station_line]
