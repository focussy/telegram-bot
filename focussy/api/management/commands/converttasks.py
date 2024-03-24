import re
from pprint import pprint

from django.core.management import BaseCommand

from focussy.api.models import Task


class Command(BaseCommand):
    def handle(self, *args, **options):
        tasks = Task.objects.filter(task_number=14)
        for task in tasks:
            answers = task.body.split("\n")[:-1]

            no_reg = re.compile(r"(\(\S+\)\S+|\S+\(\S+\))")
            pprint([no_reg.search(ans).group() for ans in answers])
            # Task.objects.create(
            #     task_number_id=15,
            #     task_type=TaskType.NUM_UNORDERED,
            #     title=task.title,
            #     body=task.body,
            #     correct_answer=task.correct_answer,
            #     answers=list(range(1, len(list((no_reg.finditer(answers.strip())))) + 1)),
            # )
            task.answers = [no_reg.search(ans).group() for ans in answers]
            task.save()
