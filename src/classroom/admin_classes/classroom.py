from django.contrib import admin

from classroom.models import Classroom


class ClassroomAdmin(admin.ModelAdmin):
    db_model = Classroom

    list_max_show_all = 100