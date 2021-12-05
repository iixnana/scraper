import random
from file_io import read_json


def random_headers():
    return random.choice(headers)


headers = read_json('headers.txt')
