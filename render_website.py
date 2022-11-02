import json
import unicodedata
from livereload import Server
from more_itertools import chunked

from jinja2 import Environment, FileSystemLoader, select_autoescape

global no_picture_gif
no_picture_gif = "./images/nopic.gif"


def fetch_json(json_file):
    with open(json_file, "r") as library_file:
        library_json = library_file.read()
    library_json_norm = unicodedata.normalize("NFKD", library_json)
    library_description = json.loads(library_json_norm)
    return library_description


def get_html_template_env():
    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html"])
        )
    template = env.get_template("template.html")
    return template


def make_library_in_columns():
    library_content = fetch_json(
        json_file="./books_description.json")
    col_length = len(library_content)//2 + 1
    columned_library = list(chunked(library_content, col_length))
    return columned_library


def on_reload():

    columned_library = make_library_in_columns()
    template = get_html_template_env()
    rendered_page = template.render(
        library=columned_library,
        no_pic=no_picture_gif,
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