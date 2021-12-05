import requests
from bs4 import BeautifulSoup
import random
from file_io import read_json, write_json


def get_new_proxies():
    response = requests.get('https://free-proxy-list.net/anonymous-proxy.html')
    soup = BeautifulSoup(response.content, "html.parser")
    proxies_list = []
    for proxy in soup.find("textarea").text[75:].strip().split("\n"):
        proxies_list.append({"http": "http://" + proxy})
    print(proxies_list)
    write_json('proxies.txt')


def random_proxy():
    return random.choice(proxies)


proxies = read_json('proxies.txt')
