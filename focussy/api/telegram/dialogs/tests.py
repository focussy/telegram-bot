import logging
from typing import TypedDict

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Cancel, Column, SwitchTo
from aiogram_dialog.widgets.text import Const, Format

from focussy.api.telegram.controllers import create_random_test
from focussy.api.telegram.states import TestSG, TestsSG

logger = logging.getLogger(__name__)


class MainWindowGetterData(TypedDict):
    message: str


async def start_random_test(
    query: CallbackQuery, button: Button, manager: DialogManager
):
    test = create_random_test()
    await manager.start(TestSG.main, data=test.pk)


tests_window = Dialog(
    Window(
        Format("Тесты"),
        Column(
            Button(
                Const("Составить случайный тест"),
                id="start_test",
                on_click=start_random_test,
            ),
            SwitchTo(
                Const("Тест по задаче <WIP>"), id="test_task", state=TestsSG.test_task
            ),
            Cancel(Const("Назад"), id="back_to_menu"),
        ),
        state=TestsSG.main,
    ),
    Window(
        Format("Тест по задаче"),
        Column(
            SwitchTo(Const("Назад"), state=TestsSG.main, id="back_to_test_menu"),
        ),
        state=TestsSG.test_task,
    ),
)
