import json
import unicodedata
from math import ceil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked


COLUMNS_ON_PAGE = 2
BOOKS_ON_PAGE = 10

def fetch_json(json_file):

    with open(json_file, "r") as library_file:
        library_description = json.load(library_file)
    return library_description


def get_html_template_env():

    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape(["html"])
        )
    template = env.get_template("template.html")
    return template


def split_page(page):

    col_length = ceil(len(page)/COLUMNS_ON_PAGE)
    columned_page = list(chunked(page, col_length))
    return columned_page


def on_reload():

    library_content = fetch_json(
        json_file="./books_description.json")
    paged_library_content = list(chunked(library_content, n=BOOKS_ON_PAGE))
    num_of_pages = len(paged_library_content)
    no_picture_gif = "./images/nopic.gif"
    template = get_html_template_env()

    for num, page in enumerate(paged_library_content, start=1):
        columned_page = split_page(page)
        page_path = str(Path(pages_folder, f"index{num}.html"))

        rendered_page = template.render(
            columned_library_page=columned_page,
            no_pic=no_picture_gif,
            num_of_pages=num_of_pages,
            page_num=num)
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
