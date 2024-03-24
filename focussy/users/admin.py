from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from focussy.users.models import User

# Register your models here.
admin.site.site_title = "Администрирование"
admin.site.index_title = "Focussy"


@admin.register(User)
class FocussyUserAdmin(UserAdmin):
    pass
