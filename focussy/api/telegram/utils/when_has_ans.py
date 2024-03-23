from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common.when import Predicate, Whenable


class WhenHasAnswers(Predicate):
    def __call__(
        self,
        data: dict,
        widget: Whenable,
        dialog_manager: DialogManager,
    ) -> bool:
        return (
            "current_task" in dialog_manager.dialog_data
            and "answers" in dialog_manager.dialog_data
        )
