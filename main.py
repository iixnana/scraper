import os
import click
from crawlers.parsers.crawler_oda import Oda
from helpers.file_io import read_text_file
from helpers.proxies import get_new_proxies


@click.group()
def cli():
    """Welcome! This is e-commerce crawler and product scraper, created for Oda's coding challenge"""


@cli.command(name='oda-crawl-limited', short_help="start crawling of Oda.com; limited urls.")
@click.option('--v', '--visits', type=int, default=10, help="provide maximum amount of link visits")
@click.option('--w', '--workers', type=int, default=5, help="provide amount of workers for parallel queues")
@click.option('--s', '--save', type=bool, is_flag=True, default=False, help="save JSON files")
@click.option('--r', '--file', type=str, default="results-limited.csv", help="results file name")
def oda_crawl_limited(v, w, s, r):
    """Crawling Oda.com. Limited amount of visits."""
    Oda().start_crawling(v, w, s, r)


@cli.command(name='oda-crawl-random-cat', short_help="start crawling of Oda.com; random category")
@click.option('--v', '--visits', type=int, default=10, help="provide maximum amount of link visits")
@click.option('--w', '--workers', type=int, default=5, help="provide amount of workers for parallel queues")
@click.option('--s', '--save', type=bool, is_flag=True, default=False, help="save JSON files")
@click.option('--r', '--file', type=str, default="results_random_cat.csv", help="results file name")
def oda_crawl_random_limited(v, w, s, r):
    """Crawling Oda.com. Limited amount of visits."""
    Oda().start_crawling_random_category(v, w, s, r)


@cli.command(name='oda-crawl-unlimited', short_help="start crawling of Oda.com")
@click.option('--w', '--workers', type=int, default=5, help="provide amount of workers for parallel queues")
@click.option('--s', '--save', type=bool, is_flag=True, default=False, help="save JSON files")
@click.option('--r', '--file', type=str, default="results_all.csv", help="results file name")
def oda_crawl_unlimited(w, s, r):
    """Crawling Oda.com. Whole website."""
    Oda().start_crawling_all(w, s, r)


@cli.command(name='oda-crawl-cat', short_help="start crawling of Oda.com; specific category")
@click.argument('category')
@click.option('--w', '--workers', type=int, default=5, help="provide amount of workers for parallel queues")
@click.option('--s', '--save', type=bool, is_flag=True, default=False, help="save JSON files")
@click.option('--r', '--file', type=str, default="results_category.csv", help="results file name")
def oda_crawl_cat(category, w, s, r):
    """Crawling Oda.com. Scrape products from whole category."""
    Oda().start_crawling_in_category(category, w, s, r)


@cli.command(name='oda-categories', short_help="start crawling of Oda.com; get all initial categories")
def oda_crawl_cat():
    """Crawling Oda.com. Scrape starting categories."""
    Oda().get_categories()


@cli.command(name='update-proxies', short_help="get new proxies")
def update_proxies():
    """Get new free proxies."""
    get_new_proxies()


if __name__ == '__main__':
    art = ""
    for line in read_text_file("./configurations/art.txt"):
        art += line
    print(art)
    os.makedirs("./results", exist_ok=True)
    cli()

