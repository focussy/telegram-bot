from typing import Any

from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Cancel, Column, Select, SwitchTo
from aiogram_dialog.widgets.text import Const, Format

from focussy.api.models import TaskNumber
from focussy.api.telegram.adapters import run_async
from focussy.api.telegram.controllers import create_task_test
from focussy.api.telegram.states import TestSG


class TaskConfigSG(StatesGroup):
    main = State()
    size = State()


async def task_numbers_getter(dialog_manager: DialogManager, **_):
    tasks_raw = [4, *range(9, 16)]
    tasks = await run_async(
        TaskNumber.objects.filter(number__in=tasks_raw).defer("subject").all
    )
    return {
        "tasks": [
            {
                "task_number": task.number,
                "task_title": task.name,
            }
            for task in tasks
        ]
    }


async def on_task_selected(
    callback: CallbackQuery, widget: Any, dialog_manager: DialogManager, item_id: str
):
    dialog_manager.dialog_data["task_number"] = int(item_id)
    await dialog_manager.switch_to(TaskConfigSG.size)


async def on_size_selected(
    callback: CallbackQuery, widget: Any, dialog_manager: DialogManager, item_id: str
):
    task_number = dialog_manager.dialog_data["task_number"]
    task_size = int(item_id)
    test = await create_task_test(task_number, task_size)
    await dialog_manager.start(TestSG.main, data=test.pk)


task_config_dialog = Dialog(
    Window(
        Const("Выберите номер задачи"),
        Column(
            Select(
                Format("{item[task_number]}. {item[task_title]}"),
                item_id_getter=lambda x: x["task_number"],
                items="tasks",
                id="task_select",
                on_click=on_task_selected,
            ),
        ),
        Cancel(Const("В главное меню"), id="back_to_tasks"),
        state=TaskConfigSG.main,
        getter=task_numbers_getter,
    ),
    Window(
        Const("Выберите размер теста"),
        Select(
            Format("{item}"),
            item_id_getter=lambda x: x,
            items=list(range(5, 21, 5)),
            id="task_size",
            on_click=on_size_selected,
        ),
        SwitchTo(Const("Назад"), id="back_to_task_config", state=TaskConfigSG.main),
        state=TaskConfigSG.size,
    ),
)
