import datetime

from django.contrib.auth import get_user_model
from django.db.models import Case, When, Value
from django.shortcuts import get_object_or_404

from app.exceptions import SubmissionException
from app.forms import SubmitAssignmentForm
from assignment.models import Assignment, AssignmentSubmission
from classroom.models import Classroom
from .tasks import send_submission

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


class SubmissionService:
    def _validate_submission(self, assignment: Assignment, user: User):
        if assignment.one_try and assignment.submissions.filter(student=user).exists():
            raise SubmissionException("Задание можно сдавать только один раз.")
        if assignment.submissions.filter(status="Проверяется", student=user).exists():
            raise SubmissionException("Задание находится на проверке.")

    def submit_task(self, form: SubmitAssignmentForm, user: User, assignment_id: int):
        assignment = get_object_or_404(Assignment, id=assignment_id)

        self._validate_submission(assignment, user)
        submission = AssignmentSubmission.objects.create(
            assignment=assignment,
            student=user,
            status="Проверяется",
            git_url=form.cleaned_data.get("url")
        )
        send_submission.delay(submission_id=submission.id)
        return submission
