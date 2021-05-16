from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

caps = [
    {
        "title": "Красная кепка",
        "price": "$ 100.00",
        "image": ""
    },
    {
        "title": "Чёрная кепка",
        "price": "$ 120.00",
        "image": "https://dvmn.org/filer/canonical/1569333143/330/"
    },
    {
        "title": "Ещё одна чёрная кепка",
        "price": "$ 90.00",
        "image": "https://dvmn.org/filer/canonical/1569333144/331/"
    },
    {
        "title": "Камуфляжная кепка",
        "price": "$ 100.00",
        "image": "https://dvmn.org/filer/canonical/1569943835/350/"
    },
    {
        "title": "Джинсовая кепка",
        "price": "$ 100.00",
        "image": "https://dvmn.org/filer/canonical/1569943835/351/"
    },
    {
        "title": "Плоская кепка",
        "price": "$ 100.00",
        "image": "https://dvmn.org/filer/canonical/1569943836/352/"
    }
]

rendered_page = template.render(caps=caps)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8001), SimpleHTTPRequestHandler)
server.serve_forever()