import logging
from typing import TypedDict

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Column
from aiogram_dialog.widgets.text import Const, Format

from focussy.api.telegram.controllers import create_random_test
from focussy.api.telegram.dialogs.task_config import TaskConfigSG
from focussy.api.telegram.states import TestSG, TestsSG

logger = logging.getLogger(__name__)


class MainWindowGetterData(TypedDict):
    message: str


async def start_random_test(
    query: CallbackQuery, button: Button, manager: DialogManager
):
    test = await create_random_test()
    await manager.start(TestSG.main, data=test.pk)


async def goto_task_config(
    query: CallbackQuery, button: Button, manager: DialogManager
):
    await manager.start(TaskConfigSG.main)


tests_window = Dialog(
    Window(
        Format("Тесты"),
        Column(
            Button(
                Const("Составить случайный тест"),
                id="start_test",
                on_click=start_random_test,
            ),
            Button(
                Const("Тест по задаче"),
                id="start_task_config",
                on_click=goto_task_config,
            ),
            Cancel(Const("Назад"), id="back_to_menu"),
        ),
        state=TestsSG.main,
    ),
)
