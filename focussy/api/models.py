from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField


# Create your models here.


class Client(models.Model):
    telegram_id = models.CharField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)

    test_attempts = models.ManyToManyField("TestSolutionAttempt")

    def __str__(self):
        return self.username


class Subject(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class TaskNumber(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    body = models.TextField()
    media = ArrayField(
        base_field=models.ImageField(upload_to="task_media"),
        null=False,
        blank=True,
        default=list,
    )
    answers = ArrayField(base_field=models.CharField(max_length=255))

    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    task_number = models.ForeignKey(TaskNumber, on_delete=models.PROTECT)

    @classmethod
    async def random(cls, task_id: int, subject_id: int = 1):
        return await cls.objects.raw(
            """
            select * from {0} limit 1 offset floor(random() * (select count(1) from {0} where subject_id = %s and task_id = %s)) where subject_id = %s and task_id = %s
        """.format(cls._meta.db_table),
            (subject_id, task_id, subject_id, task_id),
        ).afirst()

    def __str__(self):
        return str(self.pk)


class Test(models.Model):
    name = models.CharField(primary_key=True)
    tasks = models.ManyToManyField(Task)


class TestSolutionAttempt(models.Model):
    test = models.ForeignKey(Test, on_delete=models.PROTECT)

    answers = ArrayField(models.CharField(max_length=255))
    date = models.DateTimeField(auto_now_add=True)
