import requests
from bs4 import BeautifulSoup
from decouple import config
from pushbullet import Pushbullet
import time
import json
from pathlib import Path


# create file if not exists
myfile = Path('offers.json')
myfile.touch(exist_ok=True)

# notification app token from .env file
token = config("PUSHBULLET_TOKEN")
pb = Pushbullet(token)


found_products = {}

with open('offers.json', 'r') as file:
    found_products = json.load(file)


def main():
    source = requests.get(
        "https://www.olx.pl/oferty/q-call-of-duty-wwii/?search%5Bfilter_float_price%3Ato%5D=100")

    content = BeautifulSoup(source.text, 'html.parser')

    offers = content.find_all(class_="offer-wrapper")

    for product in offers:
        name = product.select_one('.title-cell h3').text.strip()
        price = product.select_one('.price strong').text.strip()
        url = product.select_one('.title-cell a')['href']

        if name not in found_products:
            found_products[name] = price
            pb.push_link(name, url, price)

    with open('offers.json', 'w+') as file:
        json.dump(found_products, file)


while True:
    main()
    # print("sprawdzam")
    time.sleep(60)
