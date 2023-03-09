from .admin_classes import admin

__all__ = [
    "admin"
]

from .admin_classes.classroom import ClassroomAdmin

from .models import Classroom

admin.site.register(Classroom, ClassroomAdmin)
