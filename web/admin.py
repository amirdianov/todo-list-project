from django.contrib import admin

from web.models import User, TaskList, TodoTask

# Register your models here.
admin.site.register(User)
admin.site.register(TaskList)
admin.site.register(TodoTask)
