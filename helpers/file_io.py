import json
from pathlib import Path
import requests
import csv

def save_html_file(title, url):
    full_file_name = title + ".html"
    if not Path(full_file_name).is_file():
        page = requests.get(url)
        with open(full_file_name, 'wb+', encoding="utf-8") as f:
            f.write(page.content)

def save_results_csv(title, products_data):
    try:
        with open(title, 'w', encoding="utf-8", newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for product in products_data.values():
                writer.writerow(product.get_data())
    except IOError:
        print("I/O error")

def read_text_file(file):
    with open(file, 'r', encoding="utf-8") as file:
        return file.readlines()

def append_line(file, line):
    with open(file, "a", encoding="utf-8") as file_object:
        file_object.write(line + "\n")

def read_json(file):
    with open(file, "r", encoding="utf-8") as json_file:
        return json.load(json_file)

def write_json(file, json_data):
    with open(file, 'w', encoding="utf-8") as outfile:
        json.dump(json_data, outfile, indent=4)

def write_json_if_not_exists(file, json_data):
    if not Path(file).is_file():
        with open(file, 'w', encoding="utf-8") as outfile:
            json.dump(json_data, outfile, indent=4)

csv_columns = [
    "id",
    "category",
    "path",
    "title",
    "extra_details",
    "brand",
    "description",
    "currency",
    "price",
    "unit_price",
    "unit",
    "size",
    "delivery_days",
    "ingredients",
    "country_of_origin",
    "place_of_origin",
    "supplier",
    "expiration",
    "pant",
    "storage",
    "variable_weight",
    "extra_tender",
    "characteristics",
    "requirements",
    "energy_kj",
    "energy_kcal",
    "saturated_fatty_acids",
    "monounsaturated_fatty_acids",
    "polyunsaturated_fatty_acids",
    "carbohydrates",
    "sugars",
    "dietary_fiber",
    "protein",
    "salt",
    "sodium",
    "polyols",
    "starch",
    "information",
    "active_substance",
    "volume",
    "roughness"
]