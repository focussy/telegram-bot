# Generated by Django 5.0.3 on 2024-03-23 14:48

import django_better_admin_arrayfield.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0006_alter_task_answers"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="test",
            name="tasks",
        ),
        migrations.AddField(
            model_name="test",
            name="tasks",
            field=django_better_admin_arrayfield.models.fields.ArrayField(
                base_field=models.IntegerField(), blank=True, default=list, size=None
            ),
        ),
    ]