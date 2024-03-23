import logging
from typing import TypedDict

from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const, Format

from focussy.api.models import Client
from focussy.api.telegram.states import StatSG
from focussy.api.telegram.utils.consts import USER_NAME

logger = logging.getLogger(__name__)


class MainWindowGetterData(TypedDict):
    message: str


async def stat_getter(dialog_manager: DialogManager, **_):
    user: Client = dialog_manager.middleware_data[USER_NAME]

    return {"solved": await user.testsolutionattempt_set.acount()}


stat_window = Dialog(
    Window(
        Format("Моя статистика"),
        Format("Выполнено тестов: {solved}"),
        Cancel(Const("Назад")),
        state=StatSG.main,
        getter=stat_getter,
    ),
)
