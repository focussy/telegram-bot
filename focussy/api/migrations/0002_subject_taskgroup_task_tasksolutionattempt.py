# Generated by Django 5.0.3 on 2024-03-22 18:28

import django.db.models.deletion
import django_better_admin_arrayfield.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0001_initial"),
    ]

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
            name="TaskGroup",
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
                ("description", models.CharField(max_length=255)),
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
                ("title", models.CharField(max_length=255, null=True)),
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
                        on_delete=django.db.models.deletion.PROTECT, to="api.taskgroup"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TaskSolutionAttempt",
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
                ("correct", models.BooleanField()),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="api.client"
                    ),
                ),
                (
                    "task",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="api.task"
                    ),
                ),
            ],
        ),
    ]