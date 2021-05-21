from http.server import HTTPServer, SimpleHTTPRequestHandler
import datetime
import collections
import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

catalog = pd.read_excel('./data/catalog.xlsx', keep_default_na=False, na_values=None).to_dict(orient='records')
products = collections.defaultdict(list)

for product in catalog:
    products[product['Категория']].append(product)


def main():
    rendered_page = template.render(
        manufactory_age=datetime.datetime.now().year-1920,
        products=products,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()
