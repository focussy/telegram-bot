import logging
from typing import TypedDict

from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Group, Start
from aiogram_dialog.widgets.text import Const, Format

from focussy.api.telegram.dialogs.stat import StatSG
from focussy.api.telegram.dialogs.tests import TestsSG

logger = logging.getLogger(__name__)


class MainSG(StatesGroup):
    main = State()
    task = State()


class MainWindowGetterData(TypedDict):
    message: str


main_window = Dialog(
    Window(
        Format("Главное меню"),
        Group(
            Start(Const("Мои задачи"), id="my_tasks", state=TestsSG.main),
            Button(Const("Все задачи"), id="tasks"),
            Start(Const("Статистика"), id="statistic", state=StatSG.main),
            width=2,
        ),
        state=MainSG.main,
    ),
)
