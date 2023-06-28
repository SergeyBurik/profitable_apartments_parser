from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import Proxy
from selenium.webdriver.common.proxy import ProxyType
from geopy.geocoders import Nominatim
from selenium.webdriver.firefox.options import Options
import pandas as pd
from parse_metro_names import get_metro_names

metro_names = get_metro_names()


class ParserQuery:
	def __init__(self, deal_type, metro_name, bedrooms, min_square=0, max_square=10 ** 5, min_price=0,
	             max_price=10 ** 9, offer_type="flat"):
		self.deal_type = deal_type
		self.metro_name = metro_name
		self.metro_id = metro_names.get(self.metro_name, "")
		self.bedrooms = bedrooms
		self.min_price = min_price
		self.max_price = max_price
		self.min_square = min_square
		self.max_square = max_square
		self.offer_type = offer_type


class Parser:
	def __init__(self, parse_query: ParserQuery):
		self.base_url = "https://www.cian.ru/cat.php?currency=2"
		self.parse_query = parse_query
		self.url = self.get_url()
		self.driver = self.init_driver()
		self.driver.get(self.url)
		self.parse()

	# self.driver.quit()

	def get_url(self):
		url = f"{self.base_url}&deal_type={self.parse_query.deal_type}&engine_version=2" \
		      f"&maxprice={self.parse_query.max_price}&minprice={self.parse_query.min_price}" \
		      f"&offer_type={self.parse_query.offer_type}&room{self.parse_query.bedrooms}=1&region=1" \
		      f"&metro%5B0%5D={self.parse_query.metro_id}"
		return url

	def init_driver(self):
		myProxy = "121.1.41.162:111"

		proxy = Proxy({
			'proxyType': ProxyType.MANUAL,
			'httpProxy': myProxy,
			'ftpProxy': myProxy,
			'sslProxy': myProxy,
			'noProxy': ''  # set this value as desired
		})

		options = Options()
		options.add_argument('--headless')
		driver = webdriver.Chrome(r'chromedriver.exe')
		return driver

	def parse(self):
		data = []

		self.driver.get(self.url)
		soup = BeautifulSoup(self.driver.page_source, "html.parser")

		apartments = soup.find_all("article", attrs={"data-name": "CardComponent"})
		for apartment in apartments:
			try:
				price = apartment.find("span", attrs={"data-mark": "MainPrice"}).text.strip()
				# address = apartment.find("div._93444fe79c--labels--L8WyJ", attrs={"data-name": "GeoLabel"}).text.strip()
				obj = {"price": price, "address": ""}
				print(obj)
				data.append(obj)
			except Exception as e:
				print(e)
		print(data)


query = ParserQuery("sale", "Авиамоторная", 2, 4 * (10 ** 6), 10 ** 7)
parser = Parser(query)
