import requests

from file_io import save_results_csv
from proxies import random_proxy
from headers import random_headers
import oda
import random
from bs4 import BeautifulSoup
import queue
from threading import Thread

starting_url = oda.starting_items_page()
visited = set()
max_visits = 10
num_workers = 5
data = {}


def get_html(url):
    try:
        proxies = random_proxy()
        headers = random_headers()
        response = requests.get(url, headers=headers, proxies=proxies)
        return response.content
    except Exception as e:
        print(e)
        return ''


def add_to_queue(links, previous_href):
    for link in links[:1]:
        if link not in visited:
            q.put((link, previous_href))


def add_product(product):
    if product.id not in data.keys():
        data[product.id] = product


def soup(html):
    return BeautifulSoup(html, "html.parser")


def crawl(href, previous_href):
    visited.add(href)
    html = get_html(oda.url(href))
    html_soup = soup(html)
    if href[:15] == "/no/categories/":
        links = oda.subcategories_soup(html_soup, href)
        pages = oda.pages_soup(html_soup, href)
        add_to_queue(pages, href)
        if links:
            random.shuffle(links)
            add_to_queue(links, href)
            return None
        products = oda.products_soup(html_soup)
        if products:
            random.shuffle(products)
            add_to_queue(products, href)
            return None
    elif href[:13] == "/no/products/":
        add_product(oda.product_details_soup(html_soup, href, previous_href))
        return None
    else:
        print("Reached unknown page: {}".format(href))


def queue_worker(i, q):
    while True:
        current_url, previous_url = q.get()
        if len(visited) < max_visits and current_url not in visited:
            crawl(current_url, previous_url)
        q.task_done()


q = queue.Queue()
for i in range(num_workers):
    Thread(target=queue_worker, args=(i, q), daemon=True).start()

visited.add(starting_url)
html = get_html(starting_url)
categories = oda.categories_soup(soup(html))
random.shuffle(categories)
for category in categories[:1]:
   q.put((category, starting_url))
q.join()

print('Done')
save_results_csv("results_live.csv", data)