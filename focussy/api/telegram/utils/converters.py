from focussy.api.models import Task


def convert_task_to_dialog(task: Task) -> dict:
    current_task = {
        "title": task.title,
        "body": task.body,
        "correct_answer": task.correct_answer,
        "task_type": task.task_type,
        "explanation": task.explanation,
    }
    if task.answers is not None:
        current_task["answers"] = [(i, answer) for i, answer in enumerate(task.answers)]

    return current_task
