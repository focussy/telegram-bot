import logging
from typing import TypedDict

from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Group, Column, SwitchTo, Cancel, Back
from aiogram_dialog.widgets.text import Const, Format


logger = logging.getLogger(__name__)


class TestsSG(StatesGroup):
    main = State()
    test_random = State()
    test_task = State()



class MainWindowGetterData(TypedDict):
    message: str


async def getter(
    dialog_manager: DialogManager,
    **_,
):

    return MainWindowGetterData(
        message="Тесты"
    )


main_window = Dialog(
    Window(
        Format(""),
        Column(
            SwitchTo(Const("Составить случайный тест"), id="test_random", state=TestsSG.test_random),
            SwitchTo(Const("Тест по задаче"), id="test_task", state=TestsSG.test_task),
            Cancel(
                Const("Назад"), id="back_to_menu"),
        ),
        state=TestsSG.main,
    ),
    Window(
        Format(""),
        Column(
            Button(Const("Составить случайный тест"), id="test_random"),
            Button(Const("Тест по задаче"), id="test_task"),
            SwitchTo(
                Const("Назад"), state=TestsSG.main, id='back_to_test_menu'),
        ),
        state=TestsSG.test_random,
    ),
    Window(
        Format(""),
        Column(
            Button(Const("Тест по задаче"), id="test_random"),
            Button(Const("Тест по задаче"), id="test_task"),
            SwitchTo(
                Const("Назад"), state=TestsSG.main, id='back_to_test_menu'),
        ),
        state=TestsSG.test_task,
    ),
)

