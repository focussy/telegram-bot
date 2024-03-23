import logging
from typing import TypedDict

from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.kbd import Column, SwitchTo, Cancel, Button
from aiogram_dialog.widgets.text import Const, Format

from focussy.api.telegram.controllers import create_random_test
from focussy.api.telegram.dialogs.test import TestSG

logger = logging.getLogger(__name__)


class TestsSG(StatesGroup):
    main = State()
    test_random = State()
    test_task = State()


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
