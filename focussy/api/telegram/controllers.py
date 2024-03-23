from focussy.api import models
from focussy.api.telegram.utils.namegenerator import get_random_name


def create_random_test(tasks: int = 21):
    """

    :param tasks: Стандартное количество задач - 26
    :return:
    """
    test = models.Test.objects.create(name=get_random_name())
    for task_number in range(1, tasks + 1):
        task = models.Task.random(task_number)
        test.tasks.add(task)
    test.save()

    return test
