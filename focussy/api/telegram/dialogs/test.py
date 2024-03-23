import logging
from typing import Any, TypedDict

from aiogram.enums import ContentType
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel, Group, Select, SwitchTo
from aiogram_dialog.widgets.text import Const, Format

from focussy.api.models import Task, Test
from focussy.api.telegram.utils.answer_validators import AnswerValidator
from focussy.api.telegram.utils.converters import convert_task_to_dialog
from focussy.api.telegram.utils.when_has_ans import WhenHasAnswers

logger = logging.getLogger(__name__)


class TestSG(StatesGroup):
    main = State()
    summary = State()
    cancel_approve = State()


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
    initial_task = await Task.objects.aget(pk=test.tasks[0])
    dialog_manager.dialog_data["test_id"] = test_id
    dialog_manager.dialog_data["current_task_number"] = 0
    dialog_manager.dialog_data["current_task"] = convert_task_to_dialog(initial_task)
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


async def validate_task(answer: str, manager: DialogManager):
    logger.warning("Answer selected: %s", answer)
    current_task_number = manager.dialog_data["current_task_number"]
    current_task = manager.dialog_data["current_task"]

    is_answer_correct = AnswerValidator.validate(
        current_task["task_type"], answer, current_task["correct_answer"]
    )
    manager.dialog_data["answers"][current_task_number] = {
        "done": True,
        "correct": is_answer_correct,
    }
    current_task_number += 1
    manager.dialog_data["current_task_number"] = current_task_number
    manager.dialog_data["current_task"] = convert_task_to_dialog(
        await Task.objects.aget(
            pk=manager.dialog_data["answers"][current_task_number]["task_id"]
        )
    )
    logger.warning("Answer is correct: %s", is_answer_correct)
    logger.warning("Correct answer: %s", current_task["correct_answer"])

    return current_task_number == len(manager.dialog_data["answers"])


async def on_ans_selected(
    callback: CallbackQuery, widget: Select, dialog_manager: DialogManager, item_id: str
):
    if await validate_task(item_id, dialog_manager):
        await dialog_manager.switch_to(state=TestSG.summary)


async def on_text_input(
    message: Message, widget: MessageInput, dialog_manager: DialogManager
):
    if await validate_task(message.text.strip(), dialog_manager):
        await dialog_manager.switch_to(state=TestSG.summary)


async def cancel_approve_getter(dialog_manager: DialogManager, **_):
    answers = dialog_manager.dialog_data["answers"]
    return {
        "done": len([answer for answer in answers if answer["done"]]),
        "tasks_number": len(answers),
    }


test_dialog = Dialog(
    Window(
        Format("{task_number}. {task_title}\n\n"),
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
            when=WhenHasAnswers(),
        ),
        SwitchTo(
            Const("Закончить тест"), state=TestSG.cancel_approve, id="cancel_approve"
        ),
        MessageInput(func=on_text_input, content_types=ContentType.TEXT),
        state=TestSG.main,
        getter=task_getter,
    ),
    Window(
        Const("Статистика"),
        Format("Выполнено {done} из {tasks_number} задач"),
        state=TestSG.summary,
    ),
    Window(
        Const(
            "Уверены что хотите закончить тест?\nПрерванные тесты не будут учитываться в статистике :("
        ),
        Format("Выполнено {done} из {tasks_number} задач"),
        Cancel(Const("Да"), id="cancel_approve_yes"),
        SwitchTo(Const("Нет"), state=TestSG.main, id="cancel_approve_no"),
        state=TestSG.cancel_approve,
        getter=cancel_approve_getter,
    ),
    on_start=on_dialog_start,
)
