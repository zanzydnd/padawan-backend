from django.contrib import admin

from .assignment import AssignmentAdmin
from .classroom import ClassroomAdmin
from classroom.models import Classroom, AssigmentProxy, AssigmentSubmissionProxy

admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(AssigmentProxy,AssignmentAdmin)
admin.site.register(AssigmentSubmissionProxy)
