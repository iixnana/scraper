import requests
from helpers.proxies import random_proxy
from helpers.headers import random_headers
from bs4 import BeautifulSoup
from abc import ABC, abstractmethod


def get_html(url):
    try:
        proxies = random_proxy()
        headers = random_headers()
        response = requests.get(url, headers=headers, proxies=proxies)
        return response.content
    except Exception as e:
        print(e)
        return ''


class Crawler(ABC):

    def add_to_queue(self, links, previous_href):
        for link in links:
            if link not in self.visited:
                self.q.put((link, previous_href))

    def add_back_to_queue(self, current_href, previous_href):
        self.q.put((current_href, previous_href))

    def add_product(self, product):
        if product.id not in self.data.keys():
            self.data[product.id] = product

    def soup(self, html):
        return BeautifulSoup(html, "html.parser")

    def queue_worker(self, i, q):
        while True:
            current_url, previous_url = q.get()
            if len(self.visited) < self.max_visits and current_url not in self.visited:
                self._crawl(current_url, previous_url)
            q.task_done()

    def queue_worker_all(self, i, q):
        while True:
            current_url, previous_url = q.get()
            if current_url not in self.visited:
                self._crawl(current_url, previous_url)
            q.task_done()

    @abstractmethod
    def _crawl(self, href, previous_href):
        pass

    @abstractmethod
    def start_crawling(self, visits, workers, flag, file):
        pass

    @abstractmethod
    def start_crawling_all(self, workers, flag, file):
        pass

    @property
    @abstractmethod
    def visited(self):
        pass

    @property
    @abstractmethod
    def max_visits(self):
        pass

    @property
    @abstractmethod
    def num_workers(self):
        pass

    @property
    @abstractmethod
    def save_flag(self):
        pass

    @property
    @abstractmethod
    def data(self, val):
        pass

    @property
    @abstractmethod
    def q(self):
        pass

