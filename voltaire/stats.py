import os

from bs4 import BeautifulSoup
from pelican import signals


def words(page):
    page_text = BeautifulSoup(page.content, "html.parser").getText()
    return len(page_text.split())


class StatsGenerator:
    def __init__(self, context, output_path, *args, **kwargs):
        self.context = context
        self.output_path = output_path

    def generate_output(self, writer):
        pages = self.context["pages"] + self.context["articles"]

        total = 0

        for page in pages:
            total += words(page)

        path = os.path.join(self.output_path, "words.txt")
        with open(path, "w", encoding="utf-8") as fd:
            fd.write(f"{total}\n")


def get_generators(_generators):
    return StatsGenerator


def register():
    signals.get_generators.connect(get_generators)
