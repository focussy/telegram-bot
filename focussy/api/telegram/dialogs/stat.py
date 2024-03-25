import logging
from typing import TypedDict

from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const, Format

from focussy.api.models import Client
from focussy.api.telegram.adapters import run_async
from focussy.api.telegram.states import StatSG
from focussy.api.telegram.utils.consts import USER_NAME

logger = logging.getLogger(__name__)


class MainWindowGetterData(TypedDict):
    message: str


async def stat_getter(dialog_manager: DialogManager, **_):
    user: Client = dialog_manager.middleware_data[USER_NAME]
    stats = await run_async(Client.get_answer_stats, user.pk)
    try:
        correct = stats[0][1]
    except IndexError:
        correct = 0
    try:
        wrong = stats[1][1]
    except IndexError:
        wrong = 0
    return {
        "solved": await run_async(user.testsolutionattempt_set.count),
        "correct": correct,
        "wrong": wrong,
    }


stat_window = Dialog(
    Window(
        Format("Моя статистика"),
        Format("Выполнено тестов: {solved}"),
        Format("Правильных ответов: {correct}"),
        Format("Неправильных ответов: {wrong}"),
        Cancel(Const("Назад")),
        state=StatSG.main,
        getter=stat_getter,
    ),
    Window(Format("Статистика по заданиям"), state=StatSG.task_stat),
)
