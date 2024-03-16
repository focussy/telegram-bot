from aiogram import Router
from aiogram.filters import (
    Command,
    CommandStart,
)
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from django.utils.translation import gettext

from focussy.api.telegram.dialogs.main import MainSG
from focussy.api.telegram.dialogs.task import TaskSG

router = Router()


@router.message(CommandStart())
async def start_handler(_: Message, dialog_manager: DialogManager):
    # Important: always set `mode=StartMode.RESET_STACK` you don't want to stack dialogs
    await dialog_manager.start(MainSG.main, mode=StartMode.RESET_STACK)


@router.message(Command("task"))
async def task_handler(_: Message, dialog_manager: DialogManager):
    await dialog_manager.start(TaskSG.main, mode=StartMode.RESET_STACK)


@router.message(Command("help"))
async def help_handler(message: Message):
    await message.answer(gettext("HelpMessage"))
