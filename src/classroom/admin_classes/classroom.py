from django.contrib import admin
from django.contrib.auth import get_user_model

from classroom.models import Classroom

User = get_user_model()


class ClassroomAdmin(admin.ModelAdmin):
    db_model = Classroom
    readonly_fields = ("unique_code",)
    filter_horizontal = ("students",)
    list_max_show_all = 100

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)

        form.base_fields["students"].queryset = User.objects.filter(status=User.UserStatus.PADAWAN)
        return form
