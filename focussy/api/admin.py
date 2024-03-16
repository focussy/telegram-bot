# Register your models here.
from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from focussy.api import models


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("username", "telegram_id")


class TaskInline(admin.StackedInline):
    model = models.Task
    extra = 0


@admin.register(models.TaskGroup)
class TaskGroupAdmin(admin.ModelAdmin):
    inlines = (TaskInline,)
    list_display = ("name", "description")
    list_display_links = ("name",)


@admin.register(models.Subject)
class SubjectAdmin(admin.ModelAdmin):
    inlines = (TaskInline,)
    list_display = ("name",)
    list_display_links = ("name",)


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ("title", "subject", "task_number")


@admin.register(models.TaskSolutionAttempt)
class TaskSolutionAttemptAdmin(admin.ModelAdmin):
    list_display = ("task", "client", "correct", "date")
