import asyncio

from focussy.api.models import TestSolutionAttempt, Test, Task
from focussy.api.telegram.adapters import run_async
from focussy.api.telegram.utils.namegenerator import get_random_name


async def create_random_test(task_numbers: list[int] | None = None):
    """

    :param task_numbers: Задачи, по которым нужен тест
    :return:
    """
    if not task_numbers:
        task_numbers = [4, *range(9, 16)]
    return await run_async(Test.objects.create,
                           name=get_random_name(),
                           tasks=[
                               t.pk
                               for t in await asyncio.gather(
                                   *[Task.get_random_number(task_number) for task_number in task_numbers]
                               )
                           ],
                           )


async def create_task_test(task_number: int, tasks: int):
    return await run_async(Test.objects.create,
        name=get_random_name(),
        tasks=[
            t.pk
            for t in await asyncio.gather(
                *[Task.get_random_number(task_number) for _ in range(tasks)]
            )
        ],
    )


async def save_attempt(user_id: int, test_id: int, rating: int, answers: list):
    await run_async(TestSolutionAttempt.objects.create,
        test_id=test_id,
        user_id=user_id,
        answers=[
            {
                "task_id": answer["task_id"],
                "done": answer["done"],
                "correct": answer["correct"],
                "answer": answer["answer"],
                "correct_answer": answer["correct_answer"],
            }
            for answer in answers
        ],
        rating=rating,
    )
