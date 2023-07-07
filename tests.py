import json
import pytest
import parser, scanner
from selenium.webdriver.chrome.webdriver import WebDriver


def get_parser_obj():
	parser_query = parser.ParserQuery("sale", "Водный стадион", 1, min_price=3 * (10 ** 6),
	                                  max_price=20 * (10 ** 6), min_square=18, max_square=45)

	parser_obj = parser.Parser(parser_query, pages=1)
	return parser_obj


def test_parser_init_driver():
	parser_obj = get_parser_obj()
	driver = parser_obj.init_driver()
	assert isinstance(driver, WebDriver)


def test_parser_get_url():
	valid_url = "https://www.cian.ru/cat.php?currency=2&deal_type=sale&engine_version=2&maxprice=20000000&" \
	            "minprice=3000000&offer_type=flat&room1=1&region=1&metro%5B0%5D=29&maxlarea=45&minlarea=18"

	parser_obj = get_parser_obj()
	url = parser_obj.get_url()
	assert url == valid_url


def test_parser_geolocate():
	parser_obj = get_parser_obj()
	res = parser_obj.geolocate([{"address": "Москва, башня Федерация"}])
	assert res == [{"address": "Москва, башня Федерация", "coordinates": [55.749618, 37.537371]}]


def test_scanner_find_neighbours():
	apartment = {"coordinates": [1, 1]}
	data = [
		{"id": "1", "coordinates": [2, 2]}, {"id": "2", "coordinates": [1, 0]}, {"id": "3", "coordinates": [1, -1]},
		{"id": "4", "coordinates": [4, 3]}, {"id": "5", "coordinates": [3, 5]}
	]
	scanner_obj = scanner.Scanner("", n_neighbours=3)
	result = scanner_obj.find_neighbours(apartment, data)
	assert sorted([el["id"] for el in result]) == sorted([data[0]["id"], data[1]["id"], data[2]["id"]])


def test_scanner_visualize_neighbours():
	try:
		scanner_obj = scanner.Scanner("", n_neighbours=5)
		scanner_obj.visualize_n_neighbours(
			[
				[{"coordinates": [0, 0]}, [
					{"coordinates": [1, 1]}, {"coordinates": [2, 1]}, {"coordinates": [1, 0]}
				]],
				[{"coordinates": [4, 3]}, [
					{"coordinates": [4, 2]}, {"coordinates": [3, 3]}, {"coordinates": [3, 4]}
				]]
			])
	except Exception as exc:
		assert False, f"'test_scanner_visualize_neighbours' raised an exception {exc}"
