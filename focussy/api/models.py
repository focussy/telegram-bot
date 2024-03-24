import random

from asgiref.sync import sync_to_async
from django.db import connection, models
from django_better_admin_arrayfield.models.fields import ArrayField


class Client(models.Model):
    telegram_id = models.CharField(primary_key=True)
    username = models.CharField(max_length=255, unique=True)

    @classmethod
    def get_answer_stats(cls, user_id: int):
        cursor = connection.cursor()
        cursor.execute(
            """
            select answer as correct, count(1) as answers
                from (select (jsonb_array_elements(at.answers) ->> 'correct') as answer
            from api_testsolutionattempt at
            where at.user_id = '507942140') as aa
            group by answer
            order by answer desc;
            """,
            (user_id,),
        )
        return cursor.fetchall()

    @classmethod
    def get_stats_by_task(cls, user_id: int, task_id: int):
        cursor = connection.cursor()
        cursor.execute("""
select answer as correct, a.number as num, count(1)
from (select (jsonb_array_elements(at.answers) ->> 'correct') as answer, (jsonb_array_elements(at.answers) ->> 'task_id') as task_id
      from api_testsolutionattempt at
      where at.user_id = '507942140') as aa
join api_task t on t.id = cast(task_id as bigint)
join api_tasknumber a on a.id = t.task_number_id
where a.number = 1
group by correct, a.number
order by correct desc
        """)
        return cursor.fetchall()

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

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"

    @classmethod
    async def get_random_number(cls, task_number: int, subject_id: int = 1):
        return random.choice(
            await sync_to_async(
                Task.objects.filter(
                    task_number__subject_id=subject_id, task_number__number=task_number
                ).all
            )()
        )


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
    user = models.ForeignKey(Client, on_delete=models.PROTECT)
    answers = models.JSONField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(null=False, blank=False)

    class Meta:
        verbose_name = "Попытка решения"
        verbose_name_plural = "Попытки решений"
