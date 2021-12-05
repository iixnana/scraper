import requests
import re
from pathlib import Path
from bs4 import BeautifulSoup

base_url = "https://oda.com"
categories_href = []
subcategories_href = []

if not Path('test.html').is_file():
    page = requests.get(base_url + "/no/products/")
    with open('test.html', 'wb+') as f:
        f.write(page.content)
else:
    print("Using existing file")

with open("test.html") as f:
    soup = BeautifulSoup(f, "html.parser")
    for categories in soup.body.find_all("a", class_="product-category__link", href=True):
        categories_href.append(categories["href"])
    if not Path('category0.html').is_file():
        page = requests.get(base_url + categories_href[0])
        with open('category0.html', 'wb+') as f:
            f.write(page.content)
    if not Path('category12.html').is_file():
        page = requests.get(base_url + categories_href[12])
        with open('category12.html', 'wb+') as f:
            f.write(page.content)
    print([(idx, item) for idx,item in enumerate(categories_href)])
with open("category0.html") as f:
    soup = BeautifulSoup(f, "html.parser")
    for subcategory in soup.body.find_all("a", href=re.compile("^"+categories_href[0]+"(.|\s)*\S(.|\s)*")):
        if not subcategory["href"] in subcategories_href:
            subcategories_href.append(subcategory["href"])
    print(subcategories_href)
    if not Path('category0sub0.html').is_file():
        page = requests.get(base_url + subcategories_href[0])
        with open('category0sub0.html', 'wb+') as f:
            f.write(page.content)
with open("category0sub0.html") as f:
    soup = BeautifulSoup(f, "html.parser")
    pages = []
    products = []
    #print(soup.body.find("div", class_=re.compile("^product-category-list")))
    for page in soup.body.find_all("a", href=re.compile("^\?page=")):
        if not page["href"] in pages:
            pages.append(page["href"])
    for product in soup.body.find_all("a", href=re.compile("^/no/products/[0-9]+(.|\s)*\S(.|\s)*")):
        products.append(product["href"])
    print(pages)
    print(products)

#More categories
subcategories_href = []

with open("category12.html") as f:
    soup = BeautifulSoup(f, "html.parser")
    for subcategory in soup.body.find_all("a", href=re.compile("^"+categories_href[12]+"(.|\s)*\S(.|\s)*")):
        if not subcategory["href"] in subcategories_href:
            subcategories_href.append(subcategory["href"])
    print(subcategories_href)
    if not Path('category12sub0.html').is_file():
        page = requests.get(base_url + subcategories_href[0])
        with open('category12sub0.html', 'wb+') as f:
            f.write(page.content)
with open("category12sub0.html") as f:
    soup = BeautifulSoup(f, "html.parser")
    print(subcategories_href[0])
    subsubcat = []
    for subsub in soup.body.find_all("a", href=re.compile("^" + subcategories_href[0] + "[0-9]+(.|\s)*\S(.|\s)*")):
        if not subsub["href"] in subsubcat:
            subsubcat.append(subsub["href"])
    print(subsubcat)
    if not Path('category12sub0sub0.html').is_file():
        page = requests.get(base_url + subsubcat[0])
        with open('category12sub0sub0.html', 'wb+') as f:
            f.write(page.content)
products = []
with open("category12sub0sub0.html") as f:
    soup = BeautifulSoup(f, "html.parser")
    pages = []
    for page in soup.body.find_all("a", href=re.compile("^\?page=")):
        if not page["href"] in pages:
            pages.append(page["href"])
    for product in soup.body.find_all("a", href=re.compile("^/no/products/[0-9]+(.|\s)*\S(.|\s)*")):
        products.append(product["href"])
    print(pages)
    print(products)
    if not Path('product_example.html').is_file():
        page = requests.get(base_url + products[0])
        with open('product_example.html', 'wb+') as f:
            f.write(page.content)
with open("product_example.html") as f:
    soup = BeautifulSoup(f, "html.parser")
    tables = soup.find_all('table')
    output=[]
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
            output.append(new_row)
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
