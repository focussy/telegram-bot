import logging
from typing import TypedDict

from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const, Format


logger = logging.getLogger(__name__)


class StatSG(StatesGroup):
    main = State()


class MainWindowGetterData(TypedDict):
    message: str


stat_window = Dialog(
    Window(
        Format("Моя статистика"),
        Cancel(Const("Назад")),
        state=StatSG.main,
    ),
)
