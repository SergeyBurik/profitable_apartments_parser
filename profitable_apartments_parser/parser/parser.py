import os
from parser.parse_metro_names import get_metro_names

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from yandex_geocoder import Client

from keywords import *

dotenv_path = os.path.join(os.getcwd(), ".env")
load_dotenv(dotenv_path)
yandex_api = os.environ.get("YANDEX_API")

metro_names = get_metro_names()


class ParserQuery:
    def __init__(
        self,
        deal_type,
        metro_name,
        bedrooms,
        min_square=0,
        max_square=10**5,
        min_price=0,
        max_price=10**9,
        offer_type="flat",
    ):
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
    def __init__(self, parse_query: ParserQuery, pages=5, browser_headless=True):
        self.base_url = "https://www.cian.ru/cat.php?currency=2"
        self.pages = pages
        self.apartments_limit = 10**6
        self.browser_headless = browser_headless
        self.parse_query = parse_query
        self.url = self.get_url()
        self.driver = self.init_driver()
        self.data = []

    def start_parser(self):
        self.data = self.parse()
        self.driver.close()

    def get_url(self):
        url = (
            f"{self.base_url}&deal_type={self.parse_query.deal_type}&engine_version=2"
            f"&maxprice={self.parse_query.max_price}&minprice={self.parse_query.min_price}"
            f"&offer_type={self.parse_query.offer_type}&room{self.parse_query.bedrooms}=1&region=1"
            f"&metro%5B0%5D={self.parse_query.metro_id}&maxlarea={self.parse_query.max_square}"
            f"&minlarea={self.parse_query.min_square}"
        )
        return url

    def init_driver(self):
        options = Options()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.headless = self.browser_headless
        driver = webdriver.Chrome(DRIVER_PATH, options=options)
        return driver

    def parse(self):
        data = []

        self.driver.get(self.url)
        soup = BeautifulSoup(self.driver.page_source, "html.parser")

        # number of apartments by query
        total_count_element_text = soup.find(
            "div", attrs={"data-name": "SummaryHeader"}
        ).text.strip()
        total_apartments = int(
            "".join([el for el in total_count_element_text if el.isnumeric()])
        )

        apartments = soup.find_all("article", attrs={"data-name": "CardComponent"})
        for i in range(1, self.pages + 1):
            if i != 1:
                self.driver.get(self.url + "&p=" + str(i))
            for apartment in apartments:
                try:
                    price = apartment.find(
                        "span", attrs={"data-mark": "MainPrice"}
                    ).text.strip()
                    price = int(price[:-2].replace(" ", ""))
                    address_elements = apartment.find_all(
                        "a", attrs={"data-name": "GeoLabel"}
                    )
                    address = ""
                    for address_element in address_elements:
                        el = address_element.contents[0]
                        if ("АО" in el) or ("р-н" in el) or ("м. " in el):
                            continue
                        address += el + ", "
                    posted_date = apartment.find(
                        "div", class_=POSTED_DATE_CLASSNAME
                    ).text.strip()
                    link = apartment.find(
                        "a", class_=APARTMENT_LINK_CLASSNAME, href=True
                    )["href"]
                    obj = {
                        "price": price,
                        "address": address[:-2],
                        "posted_date": posted_date,
                        "link": link,
                    }  # remove last ", "
                    data.append(obj)
                except Exception as e:
                    print(e)
            if len(data) >= self.apartments_limit:
                break
            if len(data) >= total_apartments:
                break
        return self.geolocate(data)

    def geolocate(self, data):
        client = Client(yandex_api)
        for apartment in data:
            try:
                coordinates = client.coordinates(apartment["address"])
                apartment["coordinates"] = [
                    float(coordinates[1]),
                    float(coordinates[0]),
                ]
            except AttributeError as e:
                print(e)
                apartment["coordinates"] = [None, None]
        return data
