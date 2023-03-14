import datetime

from django.contrib.auth import get_user_model
from django.db.models import Case, When, Value
from django.shortcuts import get_object_or_404

from assignment.models import Assignment
from classroom.models import Classroom

User = get_user_model()


class ClassroomService:
    def add_student_to_class_by_code(self, code: str, user: User) -> bool:
        class_room_obj = get_object_or_404(Classroom, unique_code=code)
        class_room_obj.students.add(user)
        return True

    def get_classroom_by_code(self, code: str):
        return get_object_or_404(Classroom, unique_code=code)

    def get_teachers_contact_info(self, classroom: Classroom):
        return User.objects.filter(head_in_classrooms=classroom).prefetch_related("possible_contacts").first()

    def get_assigments(self, classroom: Classroom):
        return Assignment.objects.filter(classroom=classroom).annotate(
            past_due_date=Case(
                When(due_to__gt=datetime.datetime.now(), then=Value(0)), default=Value(1)
            )
        ).order_by("past_due_date")


class AssigmentService:
    def get_service_by_id(self, id: int):
        return get_object_or_404(Assignment, id=id)
