# Generated by Django 5.0.3 on 2024-03-23 12:17

import django.db.models.deletion
import django_better_admin_arrayfield.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Subject",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="TaskNumber",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("number", models.IntegerField()),
                ("name", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Task",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(blank=True, max_length=255, null=True)),
                ("body", models.TextField()),
                (
                    "media",
                    django_better_admin_arrayfield.models.fields.ArrayField(
                        base_field=models.ImageField(upload_to="task_media"),
                        blank=True,
                        default=list,
                        size=None,
                    ),
                ),
                (
                    "answers",
                    django_better_admin_arrayfield.models.fields.ArrayField(
                        base_field=models.CharField(max_length=255), size=None
                    ),
                ),
                (
                    "subject",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="api.subject"
                    ),
                ),
                (
                    "task_number",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="api.tasknumber"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Test",
            fields=[
                ("name", models.CharField(primary_key=True, serialize=False)),
                ("tasks", models.ManyToManyField(to="api.task")),
            ],
        ),
        migrations.CreateModel(
            name="TestSolutionAttempt",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "answers",
                    django_better_admin_arrayfield.models.fields.ArrayField(
                        base_field=models.CharField(max_length=255), size=None
                    ),
                ),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "test",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="api.test"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Client",
            fields=[
                ("telegram_id", models.CharField(primary_key=True, serialize=False)),
                ("username", models.CharField(max_length=255, unique=True)),
                ("test_attempts", models.ManyToManyField(to="api.testsolutionattempt")),
            ],
        ),
    ]
