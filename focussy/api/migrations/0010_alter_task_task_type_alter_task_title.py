# Generated by Django 5.0.3 on 2024-03-23 16:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0009_alter_client_options_alter_subject_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="task",
            name="task_type",
            field=models.CharField(
                choices=[
                    ("text", "Text"),
                    ("text_multi", "Text Multi"),
                    ("num_unordered", "Num Unordered"),
                    ("num_ordered", "Num Ordered"),
                    ("single_choice", "Single Choice"),
                ],
                default="text",
                max_length=255,
            ),
        ),
        migrations.AlterField(
            model_name="task",
            name="title",
            field=models.TextField(blank=True, null=True),
        ),
    ]