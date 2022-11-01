import json
import unicodedata
from livereload import Server
from more_itertools import chunked

from jinja2 import Environment, FileSystemLoader, select_autoescape


def fetch_json(json_file):
    with open(json_file, "r") as library_file:
        library_json = library_file.read()
    library_json_norm = unicodedata.normalize("NFC", library_json)
    library_description = json.loads(library_json_norm)
    return library_description


def on_reload():

    library_content = fetch_json(
        json_file="./books_description.json")
    col_length = len(library_content)//2 + 1
    columned_library = list(chunked(library_content, col_length))
    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html"])
        )
    template = env.get_template("template.html")

    rendered_page = template.render(
        library=columned_library
    )
    with open("index.html", "w", encoding="utf8") as file:
        file.write(rendered_page)


def main():
    
    on_reload()
    server = Server()
    server.watch("template.html", on_reload)
    server.serve(root=".")


if __name__ == "__main__":
    main()