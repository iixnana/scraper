import requests
from bs4 import BeautifulSoup
import random
from helpers.file_io import read_json, write_json


def get_new_proxies():
    response = requests.get('https://free-proxy-list.net/anonymous-proxy.html')
    soup = BeautifulSoup(response.content, "html.parser")
    proxies_list = []
    for proxy in soup.find("textarea").text[75:].strip().split("\n"):
        proxies_list.append({"http": "http://" + proxy})
    write_json(title, proxies_list)


def random_proxy():
    return random.choice(proxies)


title = "./configurations/proxies.txt"
proxies = read_json(title)
