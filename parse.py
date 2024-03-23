from pprint import pprint

import requests
from bs4 import BeautifulSoup


def get_data(url):
    resp = requests.get(url)

    tags = resp.json()
    tasks = []
    for tag in tags['data']:
        raw_task = BeautifulSoup(tag["task_question"]["description"], features="html.parser").text
        body, title = raw_task.split("Задание 1.")
        task = {
            "title": title.strip().encode().decode('utf-8', 'ignore'),
            "body": body.strip().encode().decode('utf-8', 'ignore'),
            "correct_answer": [ans["answer"] for ans in tag["task_question"]["answers"]],
        }
        tasks.append(task)

    pprint(tasks)

    # with open("russian_v1.csv") as f:
    #     writer = csv.writer(f)
    #     for tag in tags['data']:
    #         writer.writerow(tag["task_question"])


# get_data('https://api.bank-ege.ru/api/ege/exam_tasks?subject_id=2&number=1&is_obsolete=0')
print(",".join(["1"]))