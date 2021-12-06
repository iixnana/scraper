import requests
from helpers.file_io import save_results_csv, write_json_if_not_exists
from helpers.proxies import random_proxy
from helpers.headers import random_headers
from implementations import parser_oda
import random
from bs4 import BeautifulSoup
import queue
import os
from threading import Thread


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


def queue_worker(i, q):
    while True:
        current_url, previous_url = q.get()
        if len(visited) < max_visits and current_url not in visited:
            crawl_oda(current_url, previous_url)
        q.task_done()


def crawl_oda(href, previous_href):
    visited.add(href)
    html = get_html(oda.url(href))
    html_soup = soup(html)
    is_product, var_1, var_2 = oda.scenario(href, previous_href, html_soup)
    if is_product:
        if save_flag:
            location = "./results/scraped-data" + previous_href.replace("?page=", "page-")
            os.makedirs(location, exist_ok=True)
            write_json_if_not_exists(location + var_1.id + ".txt", var_1.get_data())
        add_product(var_1)
    else:
        random.shuffle(var_1)
        add_to_queue(var_1, href)
        add_to_queue(var_2, href)


def start_crawling_oda(visits=10, workers=5, flag=False):
    global visited, max_visits, num_workers, save_flag, data, q
    visited = set()
    max_visits = visits
    num_workers = workers
    save_flag = flag
    data = {}
    q = queue.Queue()

    for i in range(num_workers):
        Thread(target=queue_worker, args=(i, q), daemon=True).start()

    starting_url = oda.starting_items_page()
    visited.add(starting_url)
    html = get_html(starting_url)
    categories = oda.categories(soup(html))
    random.shuffle(categories)
    for category in categories[:1]:
        q.put((category, starting_url))
    q.join()

    save_results_csv("./results/results_live.csv", data)
    print('Done')


