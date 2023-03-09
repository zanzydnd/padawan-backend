from django.contrib import admin
from .classroom import ClassroomAdmin
from classroom.models import Classroom, AssigmentProxy, AssigmentSubmissionProxy

admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(AssigmentProxy)
admin.site.register(AssigmentSubmissionProxy)
