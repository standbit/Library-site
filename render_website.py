import json
import unicodedata
from livereload import Server

from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape


def fetch_json(json_file):
    with open(json_file, "r") as library_file:
        library_json = library_file.read()
    library_json_norm = unicodedata.normalize("NFC", library_json)
    content = json.loads(library_json_norm)
    return content


def on_reload():
    library_content = fetch_json("./books_description.json")
    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html"])
        )
    template = env.get_template("template.html")

    rendered_page = template.render(
        library=library_content
    )
    with open("index.html", "w", encoding="utf8") as file:
        file.write(rendered_page)


def main():
    # library_content = fetch_json("./books_description.json")
    # env = Environment(
    #     loader=FileSystemLoader("."),
    #     autoescape=select_autoescape(["html"])
    #     )
    # template = env.get_template("template.html")

    # rendered_page = template.render(
    #     library=library_content
    # # )
    # with open("index.html", "w", encoding="utf8") as file:
    #     file.write(rendered_page)

    on_reload()
    server = Server()
    server.watch("template.html", on_reload)
    server.serve(root=".")
    # server = HTTPServer(("0.0.0.0", 8000), SimpleHTTPRequestHandler)
    # server.serve_forever()


if __name__ == "__main__":
    main()