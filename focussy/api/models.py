import random
from random import randint

from django.db import models
from django.db.models import Count
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
    number = models.IntegerField(unique=True)
    name = models.CharField(max_length=255, unique=True)
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.number}. {self.name}"


class Task(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
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
    task_number = models.ForeignKey(TaskNumber, on_delete=models.PROTECT)

    @staticmethod
    def random(task_number: int, subject_id: int = 1):
        return random.choice(Task.objects.filter(
            task_number__subject_id=subject_id, task_number__number=task_number
        ).all())

    def __str__(self):
        return str(self.pk)


class Test(models.Model):
    name = models.CharField(primary_key=True)
    tasks = ArrayField(models.IntegerField(), null=False, blank=True, default=list)


class TestSolutionAttempt(models.Model):
    test = models.ForeignKey(Test, on_delete=models.PROTECT)

    answers = ArrayField(models.CharField(max_length=255))
    date = models.DateTimeField(auto_now_add=True)
