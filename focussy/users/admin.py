from django.contrib import admin

from focussy.users.models import User

# Register your models here.
admin.site.register(User)
admin.site.site_title = "Администрирование"
admin.site.index_title = "Focussy"
