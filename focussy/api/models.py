import random

from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField


# Create your models here.


class Client(models.Model):
    telegram_id = models.CharField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)

    test_attempts = models.ManyToManyField("TestSolutionAttempt")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Subject(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"


class TaskNumber(models.Model):
    number = models.IntegerField(unique=True)
    name = models.CharField(max_length=255, unique=True)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.number}. {self.name}"

    class Meta:
        verbose_name = "Номер задания"
        verbose_name_plural = "Номера заданий"


class TaskType(models.TextChoices):
    TEXT = ("text",)
    TEXT_MULTI = ("text_multi",)
    NUM_UNORDERED = ("num_unordered",)
    NUM_ORDERED = ("num_ordered",)
    SINGLE_CHOICE = ("single_choice",)


class Task(models.Model):
    title = models.TextField(null=True, blank=True)
    body = models.TextField()
    media = ArrayField(
        base_field=models.ImageField(upload_to="task_media"),
        null=False,
        blank=True,
        default=list,
    )
    answers = ArrayField(
        base_field=models.CharField(max_length=255), null=True, blank=True
    )
    correct_answer = models.CharField(max_length=255, null=False, blank=False)
    explanation = models.TextField(null=True, blank=True)
    task_number = models.ForeignKey(TaskNumber, on_delete=models.PROTECT)
    task_type = models.CharField(
        max_length=255,
        choices=TaskType.choices,
        default=TaskType.TEXT,
    )

    @staticmethod
    def random(task_number: int, subject_id: int = 1):
        return random.choice(
            Task.objects.filter(
                task_number__subject_id=subject_id, task_number__number=task_number
            ).all()
        )

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"


class Test(models.Model):
    name = models.CharField(primary_key=True)
    tasks = ArrayField(models.IntegerField(), null=False, blank=True, default=list)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"


class TestSolutionAttempt(models.Model):
    test = models.ForeignKey(Test, on_delete=models.PROTECT)

    answers = ArrayField(models.CharField(max_length=255))
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Попытка решения"
        verbose_name_plural = "Попытки решений"
