from argparse import ArgumentParser

import requests
from bs4 import BeautifulSoup
from django.core.management import BaseCommand
from requests import Response


class Command(BaseCommand):
    help = "Parse sdamgia.ru"

    def __init__(self):
        super().__init__()
        self.session = requests.Session()
        self.base_url = "https://rus-ege.sdamgia.ru"
        self.base_pattern = "test?category_id={}&filter=all"
        self.skipped = 0

    def add_arguments(self, parser: ArgumentParser):
        parser.add_argument("--category_id", type=int, required=True)

    def category(self, category_id: int, skip: int) -> str:
        return f"{self.base_url}/test?category_id={category_id}&filter=all&ajax=1&skip={skip}&pages=1"

    def get_category(self, category_id: int) -> Response | None:
        try:
            return self.session.post(url=self.category(category_id, self.skipped))
        except Exception as e:
            self.stderr.write(f"Error: {e}", style_func=self.style.ERROR)
            return None

    def parse_page(self, page: Response) -> list:
        soup = BeautifulSoup(page.content, "html.parser")
        questions = soup.find_all("div", {"class": "question"})
        self.skipped += len(questions)
        return questions

    def handle(self, *args, **options):
        category_id = options.get("category_id")
        start_page = self.get_category(category_id)
        if not start_page:
            self.stderr.write(
                "Error: check the category_id. Could not parse first page",
                style_func=self.style.ERROR,
            )
            return
        while True:
            self.stdout.write(f"Parsing {category_id}")
            self.parse_page(start_page)
