import logging
from typing import TypedDict

from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Group, Start
from aiogram_dialog.widgets.text import Const, Format
from django.utils.translation import gettext

from focussy.api.telegram.dialogs.profile import ProfileSG
from focussy.api.telegram.utils import IS_NEW_NAME

logger = logging.getLogger(__name__)


class MainSG(StatesGroup):
    main = State()


class MainWindowGetterData(TypedDict):
    message: str


async def getter(
    dialog_manager: DialogManager,
    **_,
):
    is_new: bool = dialog_manager.middleware_data[IS_NEW_NAME]

    return MainWindowGetterData(
        message=(gettext("GreetNew") if is_new else gettext("Greet"))
    )


main_window = Dialog(
    Window(
        Format("{message}"),
        Group(
            Button(Const("Создать опт"), id="create_opt"),
            Button(Const("Зайти в опт"), id="get_opt"),
            Button(Const("Slon Business✨"), id="business"),
            Start(Const("Профиль"), id="profile", state=ProfileSG.main),
            Button(Const("Каталог"), id="catalogue"),
            width=2,
        ),
        state=MainSG.main,
    ),
    getter=getter,
)
