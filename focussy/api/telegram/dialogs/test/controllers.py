import logging

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button, ManagedMultiselect, Select

from focussy.api.models import Task
from focussy.api.telegram.states import TestSG
from focussy.api.telegram.utils.answer_validators import AnswerValidator
from focussy.api.telegram.utils.converters import convert_task_to_dialog

logger = logging.getLogger(__name__)


async def validate_task(answer: str, manager: DialogManager):
    current_task_number = manager.dialog_data["current_task_number"]
    current_task = manager.dialog_data["current_task"]

    is_answer_correct = AnswerValidator.validate(
        current_task["task_type"], answer, current_task["correct_answer"]
    )
    manager.dialog_data["answers"][current_task_number].update(
        {
            "done": True,
            "correct": is_answer_correct,
            "answer": answer,
            "correct_answer": current_task["correct_answer"],
        }
    )


async def on_ans_selected(
    callback: CallbackQuery,
    widget: ManagedMultiselect,
    dialog_manager: DialogManager,
    item_id: int,
):
    checked = widget.get_checked()
    dialog_manager.dialog_data["current_answer"] = sorted(
        map(lambda x: int(x) + 1, checked)
    )


async def on_ans_submitted(
    callback: CallbackQuery, widget: Button, dialog_manager: DialogManager
):
    await dialog_manager.find("task_answers").reset_checked()
    answer = "".join(map(str, dialog_manager.dialog_data["current_answer"]))
    await validate_task(answer, dialog_manager)
    await dialog_manager.switch_to(state=TestSG.answer)


async def on_next_task(
    callback: CallbackQuery, widget: Button, dialog_manager: DialogManager
):
    current_task_number = dialog_manager.dialog_data["current_task_number"]
    current_task_number += 1
    if current_task_number == len(dialog_manager.dialog_data["answers"]):
        await dialog_manager.switch_to(state=TestSG.rate_test)
        return
    dialog_manager.dialog_data["current_task_number"] = current_task_number
    dialog_manager.dialog_data["current_task"] = convert_task_to_dialog(
        await Task.objects.aget(
            pk=dialog_manager.dialog_data["answers"][current_task_number]["task_id"]
        )
    )
    await dialog_manager.switch_to(state=TestSG.main)


async def rate_test(
    event: CallbackQuery, select: Select, dialog_manager: DialogManager, data: int
):
    dialog_manager.dialog_data["rating"] = data
    await dialog_manager.switch_to(state=TestSG.summary)
