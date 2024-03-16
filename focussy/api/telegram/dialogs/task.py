import logging
from typing import TypedDict

from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Back, Group, Select
from aiogram_dialog.widgets.text import Format

from focussy.api.models import Task

logger = logging.getLogger(__name__)


class TaskSG(StatesGroup):
    main = State()


class MainWindowGetterData(TypedDict):
    task_title: str
    task_body: str
    answers: list[str]


async def getter(
    dialog_manager: DialogManager,
    **_,
):
    task = await Task.objects.aget(title="Первое")
    return MainWindowGetterData(
        task_title=task.title, task_body=task.body, answers=task.answers
    )


async def on_ans_selected(
    callback: CallbackQuery, widget: Select, manager: DialogManager, item_id: str
):
    logger.warning("Answer selected: ", item_id)


main_window = Dialog(
    Window(
        Format("{task_title}"),
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
        ),
        Back(),
        state=TaskSG.main,
        getter=getter,
    ),
)
