from typing import List
import json
import pickle

from bs4 import BeautifulSoup
import redis

from app.core.config import SITE_ENTRYPOINT
from app.products.schemas import SearchQuery, Product
from app.products.utils import get_html, log_in_console

cache = redis.Redis(host="localhost", port = 6379, db=0)

class ProductScrapping:

    def parse_products(self, html: BeautifulSoup) -> List[Product]:
        products = []

        for element in html.select('ul[class="products columns-4"] li'):

            prices = element.select(selector='bdi')
            price = prices[0].text if len(prices) else ''

            name = self.get_variable_value(element, 'div[class="addtocart-buynow-btn"] a', 'data-title')

            img_url = self.get_variable_value(element, 'noscript img', 'src')

            if not (price and name and img_url):
                continue
            products.append(Product(name=name, price=price, image_url=img_url))

        return products
    
    def get_variable_value(self, element, selector, key):
        variables = element.select(selector=selector)
        variable = variables[0].get(key, '') if len(variables) else ''
        return variable

    def get_products(self, data: SearchQuery) -> List[Product]:
        pages = data.pages if data.pages else 1
        products = []
        
        for page in range(1, pages+1):

            url = SITE_ENTRYPOINT if page == 1 else f"{SITE_ENTRYPOINT}page/{page}/"

            page_html = get_html(url=url)
            products += self.parse_products(html=page_html)
            if not products:
                break

        log_in_console("Total " + str(len(products)) + " products were scrapped in this cycle")

        rows_affected = self.update_products_in_db(products)

        log_in_console(str(rows_affected) + " rows were updated in DB")
        print("\n"*4)

        return products

    def update_products_in_db(self, products):
        products_from_db = self.get_products_from_db()
        products_to_db = []
        for product in products:
            product_cache = pickle.loads(cache.get(product.name)) if cache.get(product.name) else None
            if product_cache:
                products_to_db += self.product_to_db(product_cache, products_from_db)
            else:
                cache.set(product.name, pickle.dumps(product))
                products_to_db += self.product_to_db(product, products_from_db)
        
        self.update_products_to_db(products_from_db)

        return len(products_to_db)

    def get_products_from_db(self):
        products = []
        with open('database.json', 'r') as openfile:
            json_object = json.load(openfile)
        return products+json_object

    def product_to_db(self, product, products_from_db):
        updated_products = []
        
        if self.is_insert_request(product, products_from_db):
            updated_products.append(product)
            products_from_db.append({"name":product.name, "price":product.price, "image_url":product.image_url})
            return updated_products
        
        if self.is_update_request(product, products_from_db):
            updated_products.append(product)

        return updated_products

    def is_insert_request(self, product, products_from_db):
        for element in products_from_db:
            if product.name == element.get("name"):
                return False
        return True

    def is_update_request(self, product, products_from_db):
        for element in products_from_db:
            if product.name == element.get("name") and product.price != element.get('price'):
                element['price'] = product.price
                return True
        return False

    def get_product_from_db(self, product_to_find, products_from_db):
        for element in products_from_db:
            if product_to_find.name == element.get('name'):
                return element
        return None

    def update_products_to_db(self, products):
        json_object = json.dumps(products, indent=4)
        with open("database.json", "w") as outfile:
            outfile.write(json_object)
        return