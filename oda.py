# -*- coding: utf-8 -*-

import requests
import re
import csv
import file_io
from product import Product
from pathlib import Path
from bs4 import BeautifulSoup


def save_html_file(title, path):
    full_file_name = title + ".html"
    if not Path(full_file_name).is_file():
        page = requests.get(base_url + path)
        with open(full_file_name, 'wb+') as f:
            f.write(page.content)


def categories_file(source):
    categories_href = []
    with open(source) as f:
        soup = BeautifulSoup(f, "html.parser")
        for categories in soup.body.find_all("a", class_="product-category__link", href=True):
            categories_href.append(categories["href"])
    return categories_href


def categories_soup(soup):
    categories_href = []
    for categories in soup.body.find_all("a", class_="product-category__link", href=True):
        categories_href.append(categories["href"])
    return categories_href


def subcategories_file(category, categories_list, index):
    subcat_href = []
    with open(category) as f:
        soup = BeautifulSoup(f, "html.parser")
        for subcategory in soup.body.find_all("a", href=re.compile("^" + categories_list[index] + "(.|\s)*\S(.|\s)*")):
            if not subcategory["href"] in subcat_href:
                subcat_href.append(subcategory["href"])
    return subcat_href


def subcategories_soup(soup, href):
    subcat_href = []
    for subcategory in soup.body.find_all("a", href=re.compile("^" + href + "(.|\s)*\S(.|\s)*")):
        if not subcategory["href"] in subcat_href:
            subcat_href.append(subcategory["href"])
    return subcat_href


def products_file(subcategory):
    with open(subcategory) as f:
        soup = BeautifulSoup(f, "html.parser")
        pages = []
        products = []
        for page in soup.body.find_all("a", href=re.compile("^\?page=")):
            if not page["href"] in pages:
                pages.append(page["href"])
        for product in soup.body.find_all("a", href=re.compile("^/no/products/[0-9]+(.|\s)*\S(.|\s)*")):
            products.append(product["href"])
    return products, pages


def pages_soup(soup, href):
    pages = []
    for page in soup.body.find_all("a", href=re.compile("^\?page=")):
        if not page["href"] == "?page=1":
            pages.append(href + page["href"])
    return pages


def products_soup(soup):
    products = []
    for product in soup.body.find_all("a", href=re.compile("^/no/products/[0-9]+(.|\s)*\S(.|\s)*")):
        products.append(product["href"])
    return products


def is_product_details_page(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.body.find("div", class_="product-detail") is not None


def product_details_file(product):
    with open("product_example.html") as f:
        soup = BeautifulSoup(f, "html.parser")
        tables = soup.find_all('table')
        output = {}
        for table in tables:
            for row in table.findAll('tr'):
                new_row = []
                for cell in row.findAll(['td', 'th']):
                    for sup in cell.findAll('sup'):
                        sup.extract()

                    for collapsible in cell.findAll(
                            class_='mw-collapsible-content'):
                        collapsible.extract()
                    new_row.append(cell.get_text().strip())
                output[new_row[0]] = new_row[1]
        print(output)

        description = soup.find("p", itemprop="description")
        print(description)

        brand = soup.find("a", itemprop="brand")
        if brand is not None:
            brand_title = brand.text.strip()
            brand_id = brand["href"].replace("/no/products/brand/", "").replace("/", "").split("-")[0]
        details = products[0].replace("/no/products/", "").replace("/", "").split("-")
        id = details[0]

        title_and_extra_details = list(soup.body.find("h1").find("span").strings)
        title = title_and_extra_details[0].strip()
        extra_details = title_and_extra_details[1].strip()
        print("id {} title {} details {} brand {}".format(id, title, extra_details, brand_title))

        offers = soup.body.find("div", itemprop="offers")
        price = offers.find(itemprop="price")["content"]
        currency = offers.find(itemprop="priceCurrency")["content"]
        unit_price = offers.find("div", class_="unit-price").text.strip()
        unit = unit_price.split(" ")[-1]
        price_per_unit = unit_price.split(" ")[1]
        print(price_per_unit)
        print(unit)
        print(price)
        print(currency)
        product = Product(id, None, title, (brand_id, brand_title), description, currency, price, unit_price, unit,
                          output["StÃ¸rrelse"], output["Utleveringsdager"], output["Ingredienser"],
                          output["Opprinnelsesland"], output["LeverandÃ¸r"], output["Holdbarhetsgaranti"],
                          output["Energi"], output["Energi"], output["Fett"],
                          output["hvorav mettede fettsyrer"], output["hvorav enumettede fettsyrer"],
                          output["hvorav flerumettede fettsyrer"],
                          output["Karbohydrater"], output["hvorav sukkerarter"], output["Kostfiber"], output["Protein"],
                          output["Salt"])
        return product


def product_details_soup(soup, href, category):
    tables = soup.find_all('table')
    output = {}
    for table in tables:
        for row in table.findAll('tr'):
            new_row = []
            for cell in row.findAll(['td', 'th']):
                for sup in cell.findAll('sup'):
                    sup.extract()

                for collapsible in cell.findAll(
                        class_='mw-collapsible-content'):
                    collapsible.extract()
                new_row.append(cell.get_text().strip())
            output[dictionary[new_row[0]]] = new_row[1]

    description = soup.find("p", itemprop="description")

    brand = soup.find("a", itemprop="brand")
    if brand is not None:
        brand_title = brand.text.strip()
        brand_id = brand["href"].replace("/no/products/brand/", "").replace("/", "").split("-")[0]
        brand = (brand_id, brand_title)
    details = href.replace("/no/products/", "").replace("/", "").split("-")
    id = details[0]

    title_and_extra_details = list(soup.body.find("h1").find("span").strings)
    title = title_and_extra_details[0].strip()
    extra_details = title_and_extra_details[1].strip()

    offers = soup.body.find("div", itemprop="offers")
    price = offers.find(itemprop="price")["content"]
    currency = offers.find(itemprop="priceCurrency")["content"]
    unit_price = offers.find("div", class_="unit-price").text.strip()
    unit = unit_price.split(" ")[-1]
    price_per_unit = unit_price.split(" ")[1]
    product = Product(id, category, href, title, extra_details, brand, description, currency, price, price_per_unit,
                      unit, output)
    return product


def base_url():
    return base_url


def starting_items_page():
    return base_url + "/no/products/"


def url(href):
    return base_url + href


def scenario():
    categories_href = []
    subcategories_href = []

    save_html_file("test", "/no/products/")

    categories_href = categories_file("test.html")
    save_html_file("category0", categories_href[0])
    save_html_file("category12", categories_href[12])
    print([(idx, item) for idx, item in enumerate(categories_href)])

    subcategories_href = subcategories_file("category0.html", categories_href, 0)
    save_html_file("category0sub0", subcategories_href[0])
    # soup.body.find_all("a", href=re.compile("^" + subcategories_href[0] + "[0-9]+(.|\s)*\S(.|\s)*"))
    prod, pg = products_file("category0sub0.html")
    print(prod, pg)

    # More categories
    subcategories_href = []
    subcategories_href = subcategories_file("category12.html", categories_href, 12)
    save_html_file("category12sub0", subcategories_href[0])

    subsubcat = subcategories_file("category12sub0.html", subcategories_href, 0)
    save_html_file("category12sub0sub0", subsubcat[0])

    products = []
    products, pg = products_file("category12sub0sub0.html")
    save_html_file("product_example", products[0])

    prods = []
    prods.append(product_details_file("product_example.html"))
    save_results_csv("results.csv", prods)


base_url = "https://oda.com"
dictionary = file_io.read_json("dictionary.txt")
