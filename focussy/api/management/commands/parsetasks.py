import re

import requests
from bs4 import BeautifulSoup
from django.core.management import BaseCommand

from focussy.api.models import Task, TaskType


class Command(BaseCommand):
    help = "Parse sdamgia.ru"

    def handle(self, *args, **options):
        resp = requests.get(
            "https://api.bank-ege.ru/api/ege/exam_tasks?subject_id=2&number=13&is_obsolete=0"
        )

        tags = resp.json()
        for tag in tags["data"]:
            raw_task = BeautifulSoup(
                tag["task_question"]["description"], features="html.parser"
            )
            data = [p.text for p in raw_task.find_all("p")]
            # result_body = data[1].strip().encode().decode('utf-8', 'ignore') + '\n'
            result_body = ""
            result_title = data[0].strip().encode().decode("utf-8", "ignore")
            answers = []
            for d in data[1:]:
                formatted = d.strip().encode().decode("utf-8", "ignore")
                result_body += formatted
                splitted = formatted.split(")")
                if len(splitted) > 1:
                    answers.append(splitted[1].strip().replace("\xa0", ""))

            for i, li in enumerate(raw_task.find_all("li")):
                result_body += (
                    f"{i + 1}) {li.text.strip().encode().decode('utf-8', 'ignore')}\n"
                )
                answers.append(
                    re.search(
                        r"\(Н([ЕИ])\)\S+",
                        li.text.strip().encode().decode("utf-8", "ignore"),
                    ).group(0)
                )
            raw_explanation = BeautifulSoup(tag["comment"], features="html.parser")
            result_explanation = ""
            for d in raw_explanation.find_all("p"):
                if d is None:
                    continue
                result_explanation += (
                    d.text.strip().encode().decode("utf-8", "ignore") + "\n"
                )

            print("TITLE:", result_title)
            print("BODY:", answers)
            print(
                "CORRECT ANSWER:",
                ",".join([ans["answer"] for ans in tag["task_question"]["answers"]]),
            )
            print("EXPLANATION:", result_explanation)
            Task.objects.create(
                title=result_title,
                body=result_body,
                answers=answers,
                correct_answer=",".join(
                    [ans["answer"] for ans in tag["task_question"]["answers"]]
                ),
                task_type=TaskType.NUM_UNORDERED,
                task_number_id=13,
                explanation=result_explanation,
            )


#
