# Generated by Django 5.0.3 on 2024-03-23 10:39

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0003_test_testsolutionattempt_client_test_attempts_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="title",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
