import requests
from bs4 import BeautifulSoup
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Parse sdamgia.ru'

    def __init__(self):
        super().__init__()
        self.session = requests.Session()
        self.base_url = "https://rus-ege.sdamgia.ru"
        self.base_pattern = "test?category_id={}&filter=all"

    def category(self, category_id: int) -> str:
        return f"{self.base_url}/test?category_id={category_id}&filter=all"

    def handle(self, *args, **options):
        response = requests.get(url, cookies=self.cookies)
        soup = BeautifulSoup(response.text, "lxml")

        tasks = []
        for taskHTML in soup.findAll("div", class_="prob_maindiv"):
            task = None

            for p in taskHTML.findAll("p"):
                if p.text and p.text.strip() and not p.text.strip()[0].isdigit():
                    task = Task(p.text)
                    break

            for img in taskHTML.findAll("img"):
                src = img["src"]
                if not src.startswith("http"):
                    src = self.url_domain[:-1] + src
                task.images.add(src)

            answers = taskHTML.findAll("div", class_="answer")
            if answers:
                task.answer = answers[-1].text.rstrip(".").replace("|", "; Ответ: ").replace("&", " ")

            link = taskHTML.find("a", href=True)
            if link:
                task.task_id = link.text

            same_text = taskHTML.find("div", class_="probtext")
            if same_text and same_text.has_attr("id"):
                task.task_id = same_text["id"][4:]

            if "Впишите ответ на задание в поле выше или загрузите его" in taskHTML.parent.parent.text or \
                    "Решения заданий с развернутым ответом" in taskHTML.parent.parent.text:
                task.solutionLink = True

            tasks.append(task)
        return tasks