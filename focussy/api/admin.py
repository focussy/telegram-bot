# Register your models here.
from django.contrib import admin

from focussy.api import models


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    pass
