from typing import TypedDict


class TaskGetterData(TypedDict):
    task_number: int
    task_title: str
    task_body: str
    answers: list[tuple[str, bool]] | None


class AnswerGetterData(TypedDict):
    task_id: str
    correct: bool
    answer: str
    correct_answer: bool
    explanation: str
