from aiogram.fsm.state import State, StatesGroup


class MainSG(StatesGroup):
    summary = None
    main = State()
    task = State()


class StatSG(StatesGroup):
    main = State()


class TaskSG(StatesGroup):
    main = State()


class TestSG(StatesGroup):
    main = State()
    summary = State()
    rate_test = State()
    cancel_approve = State()


class TestsSG(StatesGroup):
    main = State()
    test_random = State()
    test_task = State()
