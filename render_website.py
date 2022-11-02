from distutils.archive_util import make_archive
import json
import unicodedata
from livereload import Server
from more_itertools import chunked

from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape


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


def make_page_in_columns(page):
    col_length = len(page)//2
    columned_page = list(chunked(page, col_length))
    return columned_page


def on_reload():
    library_content = fetch_json(
        json_file="./books_description.json")
    paged_library_content = list(chunked(library_content, 10))
    no_picture_gif = "./images/nopic.gif"
    template = get_html_template_env()
    for num, page in enumerate(paged_library_content, 1):
        columned_page = make_page_in_columns(page)
        rendered_page = template.render(
            columned_library_page=columned_page,
            no_pic=no_picture_gif)
        page_path = str(Path(pages_folder, f"index{num}.html"))
        with open(page_path, "w", encoding="utf8") as file:
            file.write(rendered_page)


def main():
    global pages_folder
    pages_folder = Path("./", "pages")
    pages_folder.mkdir(parents=True, exist_ok=True)   
    on_reload()
    server = Server()
    server.watch("template.html", on_reload)
    server.serve(root=".")


if __name__ == "__main__":
    main()