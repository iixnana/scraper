import random
from helpers.file_io import read_json


def random_headers():
    return random.choice(headers)


title = "./configurations/headers.txt"
headers = read_json(title)
