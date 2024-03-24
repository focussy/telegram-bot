from typing import Any

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.text import Case

from focussy.api.models import Task, Test
from focussy.api.telegram.controllers import save_attempt
from focussy.api.telegram.dialogs.test.dto import AnswerGetterData, TaskGetterData
from focussy.api.telegram.utils.consts import USER_NAME
from focussy.api.telegram.utils.converters import convert_task_to_dialog


async def on_dialog_start(
    start_data: Any,
    dialog_manager: DialogManager,
    **_,
):
    test_id = start_data
    test = await Test.objects.aget(pk=test_id)
    dialog_manager.dialog_data["test_id"] = test_id
    dialog_manager.dialog_data["current_task_number"] = 0
    dialog_manager.dialog_data["current_task"] = convert_task_to_dialog(
        await Task.objects.aget(pk=test.tasks[0])
    )
    dialog_manager.dialog_data["answers"] = [
        {"task_id": task_id, "done": False, "correct": False} for task_id in test.tasks
    ]


async def task_getter(dialog_manager: DialogManager, **_):
    task_number = dialog_manager.dialog_data["current_task_number"]
    task = dialog_manager.dialog_data["current_task"]
    return TaskGetterData(
        task_title=task["title"],
        task_body=task["body"],
        task_number=task_number + 1,
        answers=task["answers"] if "answers" in task else None,
    )


async def cancel_approve_getter(dialog_manager: DialogManager, **_):
    answers = dialog_manager.dialog_data["answers"]
    return {
        "done": len([answer for answer in answers if answer["done"]]),
        "tasks_number": len(answers),
    }


async def summary_getter(dialog_manager: DialogManager, **_):
    answers = dialog_manager.dialog_data["answers"]
    await save_attempt(
        test_id=dialog_manager.dialog_data["test_id"],
        user_id=dialog_manager.middleware_data[USER_NAME].pk,
        answers=answers,
        rating=dialog_manager.dialog_data["rating"],
    )

    return {
        "done": len([answer for answer in answers if answer["done"]]),
        "tasks_number": len(answers),
        "errors": [
            (i, err["answer"], err["correct_answer"])
            for i, err in enumerate(answers)
            if not err["correct"]
        ],
    }


async def answer_getter(dialog_manager: DialogManager, **_):
    task_number = dialog_manager.dialog_data["current_task_number"]
    answer = dialog_manager.dialog_data["answers"][task_number]
    current_task = dialog_manager.dialog_data["current_task"]
    return AnswerGetterData(
        task_id=task_number + 1,
        answer=answer["answer"],
        correct_answer=current_task["correct_answer"],
        explanation=current_task["explanation"],
        correct=answer["correct"],
    )


def has_explanation_selector(
    data: dict, case: Case, dialog_manager: DialogManager
) -> bool:
    return (
        "explanation"
        in dialog_manager.dialog_data["answers"][
            dialog_manager.dialog_data["current_task_number"]
        ]
    )
