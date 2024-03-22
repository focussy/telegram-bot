import logging
from typing import TypedDict

from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Group, Column, SwitchTo
from aiogram_dialog.widgets.text import Const, Format
from django.utils.translation import gettext

from focussy.api.telegram.utils import IS_NEW_NAME

logger = logging.getLogger(__name__)


class MainSG(StatesGroup):
    main = State()
    task = State()


class MainWindowGetterData(TypedDict):
    message: str


async def getter(
    dialog_manager: DialogManager,
    **_,
):

    return MainWindowGetterData(
        message="Главное меню"
    )


main_window = Dialog(
    Window(
        Format("Главное меню"),
        Group(
            Button(Const("Мои задачи"), id="my_tasks"),
            Button(Const("Задачи"), id="tasks"),
            Button(Const("Статистика"), id="statistic"),
            width=2,
        ),
        state=MainSG.main,
    ),
    Window(
        Format(""),
        Column(
            Button(Const("Составить случайный тест"), id="test_random"),
            Button(Const("Тест по задаче"), id="test_task"),
            SwitchTo(
                Const("Назад"), id="back_to_menu", state=MainSG.main
            ),
        ),
        state=MainSG.task,
    ),
)

