# Register your models here.
from django.contrib import admin
from django_better_admin_arrayfield.admin.mixins import DynamicArrayMixin

from focussy.api import models


admin.site.title = "Focussy Admin"


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("username", "telegram_id")


class TaskInline(admin.StackedInline):
    model = models.Task
    extra = 0


@admin.register(models.TaskNumber)
class TaskNumberAdmin(admin.ModelAdmin):
    inlines = (TaskInline,)
    list_display = ("number", "name", "get_subject")

    def get_subject(self, instance: models.TaskNumber):
        return instance.subject.name

    list_display_links = ("name",)


@admin.register(models.Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_display_links = ("name",)


@admin.register(models.Task)
class TaskAdmin(admin.ModelAdmin, DynamicArrayMixin):
    list_display = ("title", "task_number", "get_subject")

    list_filter = ("task_number__number", )

    def get_subject(self, instance: models.Task):
        return instance.task_number.subject.name


@admin.register(models.Test)
class TestAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TestSolutionAttempt)
class TestSolutionAttemptAdmin(admin.ModelAdmin):
    pass
