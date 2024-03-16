from django.db import models
from django_better_admin_arrayfield.models.fields import ArrayField


# Create your models here.


class Client(models.Model):
    telegram_id = models.CharField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.username


class Subject(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class TaskGroup(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Task(models.Model):
    title = models.CharField(max_length=255, null=True)
    body = models.TextField()
    media = ArrayField(
        base_field=models.ImageField(upload_to="task_media"),
        null=False,
        blank=True,
        default=list,
    )
    answers = ArrayField(base_field=models.CharField(max_length=255))

    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    task_number = models.ForeignKey(TaskGroup, on_delete=models.PROTECT)

    def __str__(self):
        return str(self.pk)


class TaskSolutionAttempt(models.Model):
    task = models.ForeignKey(Task, on_delete=models.PROTECT)
    client = models.ForeignKey(Client, on_delete=models.PROTECT)

    correct = models.BooleanField()
    date = models.DateTimeField(auto_now_add=True)
