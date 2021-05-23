from http.server import HTTPServer, SimpleHTTPRequestHandler
import argparse
import datetime
import collections
import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filepath', default='./data/catalog.xlsx')

    return parser


def open_catalog(file):
    catalog = pd.read_excel(file, keep_default_na=False, na_values=None).to_dict(orient='records')
    products = collections.defaultdict(list)

    for product in catalog:
        products[product['Категория']].append(product)

    return products


def create_template():
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    rendered_page = template.render(
        manufactory_age=datetime.datetime.now().year-1920,
        products=products,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)


def run_server():
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


def main():
    parser = createParser()
    namespace = parser.parse_args()

    print(namespace)

    products = open_catalog(namespace.filepath)
    create_template()
    run_server()


if __name__ == '__main__':
    main()
