from helpers.file_io import save_results_csv, write_json_if_not_exists, create_all_results_file, append_product_csv, \
    write_text_file
from crawlers.parsers import parser_oda as parser
import random
import queue
import os
import time
from threading import Thread
from crawlers.crawler import Crawler, get_html


class Oda(Crawler):

    def _crawl(self, href, previous_href):
        self.visited.add(href)
        html = get_html(parser.url(href))
        html_soup = super().soup(html)
        is_product, var_1, var_2 = parser.scenario(href, previous_href, html_soup)
        if is_product is None and var_1 is None and var_2 is None:
            self.visited.discard(href)
            super().add_back_to_queue(href, previous_href)
        elif is_product:
            if self.save_flag:
                location = "./results/scraped-data" + previous_href.replace("?page=", "page-")
                os.makedirs(location, exist_ok=True)
                write_json_if_not_exists(location + var_1.id + ".txt", var_1.get_data())
            super().add_product(var_1)
        else:
            random.shuffle(var_1)
            super().add_to_queue(var_1, href)
            super().add_to_queue(var_2, href)

    def _crawl_all(self, href, previous_href):
        self.visited.add(href)
        time.sleep(1)
        html = get_html(parser.url(href))
        html_soup = super().soup(html)
        is_product, var_1, var_2 = parser.scenario(href, previous_href, html_soup)
        if is_product is None and var_1 is None and var_2 is None:
            self.visited.discard(href)
            super().add_back_to_queue(href, previous_href)
        elif is_product:
            append_product_csv(self.results_file, var_1)
        else:
            random.shuffle(var_1)
            super().add_to_queue(var_1, href)
            super().add_to_queue(var_2, href)

    def start_crawling(self, visits=10, workers=5, flag=False, results_file="results.csv"):
        self.visited = set()
        self.max_visits = visits
        self.num_workers = workers
        self.save_flag = flag
        self.data = {}
        self.q = queue.Queue()

        for i in range(self.num_workers):
            Thread(target=super().queue_worker, args=(i, self.q), daemon=True).start()

        starting_url = parser.starting_items_page()
        self.visited.add(starting_url)
        html = get_html(starting_url)
        categories = parser.categories(super().soup(html))
        random.shuffle(categories)
        for category in categories:
            self.q.put((category, starting_url))
        self.q.join()

        results_file = "./results/" + results_file
        save_results_csv(results_file, self.data)
        print("Crawling is completed. Find results at {}".format(results_file))
        print("Visited: {}".format(self.visited))

    def start_crawling_random_category(self, visits=10, workers=5, flag=False, results_file="results.csv"):
        self.visited = set()
        self.max_visits = visits
        self.num_workers = workers
        self.save_flag = flag
        self.data = {}
        self.q = queue.Queue()

        for i in range(self.num_workers):
            Thread(target=super().queue_worker, args=(i, self.q), daemon=True).start()

        starting_url = parser.starting_items_page()
        self.visited.add(starting_url)
        html = get_html(starting_url)
        categories = parser.categories(super().soup(html))
        self.q.put((random.choice(categories), starting_url))
        self.q.join()

        results_file = "./results/" + results_file
        save_results_csv(results_file, self.data)
        print('Crawling is completed. Find results at {}'.format(results_file))
        print("Visited: {}".format(self.visited))

    def start_crawling_all(self, workers=5, flag=False, results_file="results_all.csv"):
        self.visited = set()
        self.num_workers = workers
        self.save_flag = flag
        self.data = {}
        self.q = queue.Queue()
        self.results_file = "./results/" + results_file
        create_all_results_file(self.results_file)

        for i in range(self.num_workers):
            Thread(target=super().queue_worker_all_save, args=(i, self.q), daemon=True).start()

        starting_url = parser.starting_items_page()
        self.visited.add(starting_url)
        html = get_html(starting_url)
        categories = parser.categories(super().soup(html))
        random.shuffle(categories)
        for category in categories:
            self.q.put((category, starting_url))
        self.q.join()

        print('Crawling is completed. Find results at {}'.format(results_file))
        print("Visited: {}".format(self.visited))

    def start_crawling_in_category(self, category, workers=5, flag=False, results_file="category_results.csv"):
        self.visited = set()
        self.num_workers = workers
        self.save_flag = flag
        self.data = {}
        self.q = queue.Queue()

        for i in range(self.num_workers):
            Thread(target=super().queue_worker_all, args=(i, self.q), daemon=True).start()

        starting_url = parser.url(category)
        self.visited.add(starting_url)
        html = get_html(starting_url)
        subcategories = parser.subcategories(super().soup(html), category)
        random.shuffle(subcategories)
        for subcategory in subcategories:
            self.q.put((subcategory, starting_url))
        self.q.join()

        results_file = "./results/" + results_file
        save_results_csv(results_file, self.data)
        print('Crawling is completed. Find results at {}'.format(results_file))
        print("Visited: {}".format(self.visited))

    def get_categories(self):
        starting_url = parser.starting_items_page()
        self.visited.add(starting_url)
        html = get_html(starting_url)
        categories = parser.categories(super().soup(html))
        for category in categories:
            print(category)
        write_text_file("categories.txt", categories)

    visited = set()
    max_visits = 10
    num_workers = 5
    save_flag = False
    data = {}
    q = queue.Queue()
    results_file = ""
