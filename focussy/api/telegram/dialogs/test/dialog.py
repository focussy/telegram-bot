from aiogram_dialog import Dialog, StartMode, Window
from aiogram_dialog.widgets.kbd import (
    Back,
    Button,
    Cancel,
    Column,
    Multiselect,
    Select,
    Start,
    SwitchTo,
)
from aiogram_dialog.widgets.text import Case, Const, Format, List

from focussy.api.telegram.dialogs.test.controllers import (
    on_ans_selected,
    on_ans_submitted,
    on_next_task,
    rate_test,
)
from focussy.api.telegram.dialogs.test.getters import (
    answer_getter,
    cancel_approve_getter,
    has_explanation_selector,
    on_dialog_start,
    summary_getter,
    task_getter,
)
from focussy.api.telegram.states import MainSG, TestSG
from focussy.api.telegram.utils.when_has_ans import WhenHasAnswers

test_dialog = Dialog(
    Window(
        Format("{task_number}. {task_title}\n\n"),
        Format("{task_body}"),
        Column(
            Multiselect(
                Format("☑️ {item[1]}"),
                Format("{item[1]}"),
                items="answers",
                id="task_answers",
                item_id_getter=lambda x: x[0],
                on_state_changed=on_ans_selected,
            ),
            when=WhenHasAnswers(),
        ),
        Button(Const("Далее"), id="next_task", on_click=on_ans_submitted),
        SwitchTo(
            Const("Закончить тест"), state=TestSG.cancel_approve, id="cancel_approve"
        ),
        state=TestSG.main,
        getter=task_getter,
    ),
    Window(
        Format("Задание {task_id}"),
        Case(
            {
                True: Format("Ваш ответ: {answer} ✅"),
                False: Format("Ваш ответ: {answer} 🅾️"),
            },
            selector="correct",
        ),
        Format("Правильный ответ: {correct_answer}"),
        Case(
            {True: Format("⚠️ Пояснение: \n{explanation}"), False: Const("")},
            selector=has_explanation_selector,
        ),
        Button(Const("Далее"), id="next_task", on_click=on_next_task),
        SwitchTo(
            Const("Закончить тест"), state=TestSG.cancel_approve, id="cancel_approve"
        ),
        state=TestSG.answer,
        getter=answer_getter,
    ),
    Window(
        Const("Оцените тест!"),
        Select(
            Format("{item}"),
            items=lambda _: list(range(1, 6)),
            id="task_rate",
            item_id_getter=lambda x: x,
            on_click=rate_test,
        ),
        state=TestSG.rate_test,
    ),
    Window(
        Const("Статистика"),
        Format("Выполнено {done} из {tasks_number} задач"),
        Format("Ошибки:"),
        List(
            Format("* {item[0]}. Правильный ответ: {item[1]}. Ваш ответ: {item[2]}. 🅾️"),
            items="errors",
        ),
        Cancel(Const("К выбору задач"), id="back_to_tasks"),
        Start(
            Const("В главное меню"),
            id="to_main_menu",
            state=MainSG.main,
            mode=StartMode.RESET_STACK,
        ),
        state=TestSG.summary,
        getter=summary_getter,
    ),
    Window(
        Const(
            "Уверены что хотите закончить тест?\nПрерванные тесты не будут учитываться в статистике :("
        ),
        Format("Выполнено {done} из {tasks_number} задач"),
        Cancel(Const("Да"), id="cancel_approve_yes"),
        Back(Const("Нет"), id="cancel_approve_no"),
        state=TestSG.cancel_approve,
        getter=cancel_approve_getter,
    ),
    on_start=on_dialog_start,
)
