import logging
from typing import TypedDict

from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Group
from aiogram_dialog.widgets.text import Const, Format
from django.utils.translation import gettext


logger = logging.getLogger(__name__)


class ProfileSG(StatesGroup):
    main = State()


class MainWindowGetterData(TypedDict):
    message: str


async def getter(
    dialog_manager: DialogManager,
    **_,
):
    return MainWindowGetterData(message=(gettext("Profile")))


main_window = Dialog(
    Window(
        Format("{message}"),
        Group(
            Button(Const("Создать опт"), id="create_opt"),
            Button(Const("Каталог"), id="catalogue"),
            width=2,
        ),
        state=ProfileSG.main,
    ),
    getter=getter,
)
