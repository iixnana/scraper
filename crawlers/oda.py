from helpers.file_io import save_results_csv, write_json_if_not_exists
from parsers import oda as parser
import random
import queue
import os
from threading import Thread
from crawlers.crawler import crawler


class oda(crawler):

    def crawl(self, href, previous_href):
        self.visited.add(href)
        html = super().get_html(parser.url(href))
        html_soup = super().soup(html)
        is_product, var_1, var_2 = parser.scenario(href, previous_href, html_soup)
        if is_product:
            if self.save_flag:
                location = "./results/scraped-data" + previous_href.replace("?page=", "page-")
                os.makedirs(location, exist_ok=True)
                write_json_if_not_exists(location + var_1.id + ".txt", var_1.get_as_dict())
            super().add_product(var_1)
        else:
            random.shuffle(var_1)
            super().add_to_queue(var_1, href)
            super().add_to_queue(var_2, href)

    def start_crawling(self, visits=10, workers=5, flag=False):

        for i in range(self.num_workers):
            Thread(target=super().queue_worker, args=(i, self.q), daemon=True).start()

        starting_url = parser.starting_items_page()
        self.visited.add(starting_url)
        html = super().get_html(starting_url)
        categories = parser.categories(super().soup(html))
        random.shuffle(categories)
        for category in categories[:1]:
            self.q.put((category, starting_url))
        self.q.join()

        save_results_csv("./results/results_live.csv", self.data)
        print('Done')

    visited = set()
    max_visits = 10
    num_workers = 5
    save_flag = False
    data = {}
    q = queue.Queue()
