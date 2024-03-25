import logging
from typing import TypedDict

from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Group, Start
from aiogram_dialog.widgets.text import Const, Format

from focussy.api.telegram.states import MainSG, StatSG, TestsSG

logger = logging.getLogger(__name__)


class MainWindowGetterData(TypedDict):
    message: str


main_window = Dialog(
    Window(
        Format("Главное меню"),
        Group(
            Start(Const("Мои задачи"), id="my_tasks", state=TestsSG.main),
            Start(Const("Статистика"), id="statistic", state=StatSG.main),
            width=2,
        ),
        state=MainSG.main,
    ),
)
