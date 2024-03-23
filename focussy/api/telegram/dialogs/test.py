import logging
from typing import Any, TypedDict

from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Cancel, Group, Select
from aiogram_dialog.widgets.text import Const, Format

from focussy.api.models import Test
from focussy.api.telegram.utils.when_has_ans import WhenHasAnswers

logger = logging.getLogger(__name__)


class TestSG(StatesGroup):
    main = State()


class TaskGetterData(TypedDict):
    task_number: int
    task_title: str
    task_body: str
    answers: list[tuple[str, bool]] | None


async def on_dialog_start(
    start_data: Any,
    dialog_manager: DialogManager,
    **_,
):
    test_id = start_data
    test = await Test.objects.aget(pk=test_id)
    initial_task = test.tasks.first()
    dialog_manager.dialog_data["test_id"] = test_id
    dialog_manager.dialog_data["tasks_number"] = test.tasks.count()
    dialog_manager.dialog_data["current_task_number"] = 0
    current_task = {
        "title": initial_task.title,
        "body": initial_task.body,
        "correct_answer": initial_task.correct_answer,
    }
    if initial_task.answers is not None:
        current_task["answers"] = [answer for answer in initial_task.answers]
    dialog_manager.dialog_data["current_task"] = current_task
    dialog_manager.dialog_data["answers"] = [
        False for _ in range(dialog_manager.dialog_data["tasks_number"])
    ]


async def task_getter(dialog_manager: DialogManager, **_):
    task_number = dialog_manager.dialog_data["current_task_number"]
    test = await Test.objects.aget(pk=dialog_manager.dialog_data["test_id"])
    task = await test.tasks.aget(task_number=task_number)
    return TaskGetterData(
        task_title=task["title"],
        task_body=task["body"],
        task_number=dialog_manager.dialog_data["current_task_number"],
        answers=task["answers"] if task["answers"] is not None else [],
    )


async def on_ans_selected(
    callback: CallbackQuery, widget: Select, manager: DialogManager, item_id: str
):
    logger.warning("Answer selected: ", item_id)
    current_task_number = manager.dialog_data["current_task_number"]
    current_task = manager.dialog_data["current_task"]

    manager.dialog_data["answers"][current_task_number] = (
        item_id in current_task["correct_answer"]
    )
    logger.warning("Current task: ", manager.dialog_data["current_task"])
    logger.warning("Answer: ", item_id in current_task["correct_answer"])
    manager.dialog_data["current_task_number"] = (
        manager.dialog_data["current_task_number"] + 1
    )

    await manager.update({})


test_dialog = Dialog(
    Window(
        Format("{task_number} {task_title}"),
        Format("{task_body}"),
        Group(
            Select(
                Format("{item}"),
                items="answers",
                id="task_answers",
                item_id_getter=lambda x: x,
                on_click=on_ans_selected,
            ),
            width=2,
            when=WhenHasAnswers,
        ),
        Cancel(Const("Закончить тест")),
        state=TestSG.main,
        getter=task_getter,
    ),
    on_start=on_dialog_start,
)
