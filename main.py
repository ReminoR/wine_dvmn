import argparse
import collections
import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape

YEAR_FOUNDATION = 1920


def createParser():
    parser = argparse.ArgumentParser(description='The application prepairs web-server for site')
    parser.add_argument('-f', '--filepath', default='./data/catalog.xlsx', help='Path to file of catalog products (.xlsx)')

    return parser


def open_catalog(filepath):
    catalog = pd.read_excel(filepath, keep_default_na=False, na_values=None).to_dict(orient='records')
    products = collections.defaultdict(list)

    for product in catalog:
        products[product['Категория']].append(product)

    return products


def get_template():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    return template


def render_page(template, manufactory_age, products):
    rendered_page = template.render(
        manufactory_age=manufactory_age,
        products=products,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def run_server():
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


def main():
    manufactory_age = datetime.datetime.now().year - YEAR_FOUNDATION

    parser = createParser()
    namespace = parser.parse_args()
    products = open_catalog(namespace.filepath)
    template = get_template()
    render_page(template, manufactory_age, products)
    run_server()


if __name__ == '__main__':
    main()
