from argparse import ArgumentParser
from pprint import pprint

import requests
from bs4 import BeautifulSoup
from django.core.management import BaseCommand
from requests import Response

from focussy.api.models import Task, TaskType


class Command(BaseCommand):
    help = "Parse sdamgia.ru"

    def handle(self, *args, **options):
        resp = requests.get('https://api.bank-ege.ru/api/ege/exam_tasks?subject_id=2&number=2&is_obsolete=0')

        tags = resp.json()
        for tag in tags['data']:
            raw_task = BeautifulSoup(tag["task_question"]["description"], features="html.parser")
            # pprint(raw_task.p.text)
            data = [p.text for p in raw_task.find_all("p")]
            result_body = data[0].strip().encode().decode('utf-8', 'ignore') + '\n'
            result_title = ""
            title_start = False
            for d in data[1:]:
                formatted = d.strip().encode().decode('utf-8', 'ignore')
                if len(formatted) > 0 and formatted != "":
                    if "Задание 2." in formatted:
                        title_start = True
                    if title_start:
                        result_title += formatted + "\n"
                        continue
                    result_body += formatted
            raw_explanation = BeautifulSoup(tag["comment"], features="html.parser")
            result_explanation = ""
            for d in raw_explanation.find_all("p"):
                if d is None:
                    continue
                result_explanation += d.text.strip().encode().decode('utf-8', 'ignore') + '\n'

            print("TITLE:", result_title)
            print("BODY:", result_body)
            print("CORRECT ANSWER:", ",".join([ans["answer"] for ans in tag["task_question"]["answers"]]),)
            print("EXPLANATION:", result_explanation)
            Task.objects.create(
                title=result_title,
                body=result_body,
                correct_answer=",".join([ans["answer"] for ans in tag["task_question"]["answers"]]),
                task_type=TaskType.NUM_UNORDERED,
                task_number_id=2,
                explanation=result_explanation,
            )
