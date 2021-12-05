import re
from helpers import file_io
from models.oda.product import Product


def categories(soup):
    category_paths = []
    for category in soup.body.find_all("a", class_="product-category__link", href=True):
        category_paths.append(category["href"])
    return category_paths


def subcategories(soup, href):
    subcategory_paths = []
    for subcategory in soup.body.find_all(href=re.compile("^" + href + "(.|\s)*\S(.|\s)*")):
        if not subcategory["href"] in subcategory_paths:
            subcategory_paths.append(subcategory["href"])
    return subcategory_paths


def pages(soup, href):
    page_paths = []
    pattern = "\?page="
    for page in soup.body.find_all("a", href=re.compile("^\?page="), title="Neste side"):
        if pattern not in href:
            page_paths.append(href + page["href"])
        else:
            ind = href.index(pattern)
            page_paths.append(href[:ind]+page["href"])
    return page_paths


def products(soup):
    product_paths = []
    for product in soup.body.find_all("a", href=re.compile("^/no/products/[0-9]+(.|\s)*\S(.|\s)*")):
        product_paths.append(product["href"])
    return product_paths


def product_details(soup, href, category):
    product_data = extract_table_data(soup.find_all('table'))

    brand = soup.find("a", itemprop="brand")
    if brand is not None:
        brand_title = brand.text.strip()
        brand_id = brand["href"].replace("/no/products/brand/", "").replace("/", "").split("-")[0]
        brand = (brand_id, brand_title)

    title_and_extra_details = list(soup.body.find("h1").find("span").strings)
    offers = soup.body.find("div", itemprop="offers")
    unit_price = offers.find("div", class_="unit-price").text.strip()

    return Product(
        {
            "path": href,
            "id": href.replace("/no/products/", "").replace("/", "").split("-")[0],
            "title": title_and_extra_details[0].strip(),
            "extra_details": title_and_extra_details[1].strip(),
            "brand": brand,
            "description": soup.find("p", itemprop="description"),
            "price": offers.find(itemprop="price")["content"],
            "currency": offers.find(itemprop="priceCurrency")["content"],
            "unit": unit_price.split(" ")[-1],
            "price_per_unit": unit_price.split(" ")[1],
            "category": category
        } | product_data
    )


def extract_table_data(tables):
    product_data = {}
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
            if new_row[0] in dictionary.keys():
                product_data[dictionary[new_row[0]]] = new_row[1]
            else:
                file_io.append_line("./configurations/missing_keys.txt", new_row[0])
    return product_data


def base_url():
    return base_url


def starting_items_page():
    return base_url + "/no/products/"


def url(href):
    return base_url + href


def scenario(href, previous_href, soup):
    if href.startswith("/no/categories/"):
        category_paths = subcategories(soup, href)
        page_paths = pages(soup, href)
        if category_paths:
            return False, category_paths, page_paths
        product_paths = products(soup)
        if product_paths:
            return False, product_paths, page_paths
    elif href.startswith("/no/products/"):
        return True, product_details(soup, href, previous_href), None
    return None, None, None


base_url = "https://oda.com"
dictionary = file_io.read_json("./configurations/dictionary.txt")
