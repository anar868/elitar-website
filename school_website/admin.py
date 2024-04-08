from django.contrib import admin
from . import models

admin.site.register(models.User)
admin.site.register(models.MissingStudents)
admin.site.register(models.Checked)
admin.site.register(models.Student)
admin.site.register(models.Class)

