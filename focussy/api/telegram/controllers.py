from django.db import transaction
from focussy.api import models
from focussy.api.telegram.utils.namegenerator import get_random_name


@transaction.atomic
async def create_random_test(tasks: int = 26):
    """

    :param tasks: Стандартное количество задач - 26
    :return:
    """
    test = await models.Test.objects.acreate(name=get_random_name())
    for task_number in range(tasks):
        task = await models.Task.random()
        test.tasks.add(task)
    await test.asave()

    return test
