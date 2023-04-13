from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DetailView, ListView

from assignment.models import Assignment, AssignmentSubmission, AlgSubmissionResults
from classroom.models import Classroom
from .forms import SignUpForm, SubmitAssignmentForm
from .services import ClassroomService, AssigmentService, SubmissionService
from .tasks import send_submission


class CustomLoginView(LoginView):
    template_name = "app/auth/login.html"
    success_url = "/"

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main_page")
        return super().get(request, *args, **kwargs)


@login_required
def logout_view(request):
    logout(request)
    return redirect("/")


# Sign Up View
class SignUpView(CreateView):
    form_class = SignUpForm
    success_url = "/auth"
    template_name = 'app/auth/register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("main_page")
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form_class()(request.POST)
        if form.is_valid():
            form.save()
            return redirect("auth")
        else:
            return render(request, self.template_name, {"form": form})


class IndexView(LoginRequiredMixin, View):
    login_url = "/auth"
    service = ClassroomService()

    def get(self, request):
        return render(request, "app/index.html")

    def post(self, request):
        code = request.POST.get("code")

        if not code:
            return redirect("main_page")

        self.service.add_student_to_class_by_code(code, request.user)
        return redirect("main_page")  # TODO: добавить редирект на страницу класса


class ClassroomListView(LoginRequiredMixin, ListView):
    login_url = "/auth"
    model = Classroom
    template_name = "app/classes_list.html"

    def get_queryset(self):
        return self.model.objects.filter(students=self.request.user)


class ClassroomDetailView(LoginRequiredMixin, DetailView):
    model = Classroom
    login_url = "/auth"
    template_name = "app/class_detail.html"
    service = ClassroomService()

    def get_object(self, queryset=None):
        return self.service.get_classroom_by_code(code=self.kwargs.get("unique_code"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["teacher"] = self.service.get_teachers_contact_info(self.object)
        context["assignments"] = self.service.get_assigments(classroom=self.object)
        return context


class AssignmentListView(LoginRequiredMixin, ListView):
    login_url = "/auth"
    model = Assignment
    template_name = "app/task_list.html"

    def get_queryset(self):
        return self.model.objects.filter(classroom__students=self.request.user).order_by("-created_at")


class AssignmentDetailView(LoginRequiredMixin, DetailView):
    login_url = "/auth"
    model = Assignment
    template_name = "app/task_detail.html"
    service = AssigmentService()

    def get_object(self, queryset=None):
        return self.service.get_service_by_id(id=self.kwargs.get("pk"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["submissions"] = AssignmentSubmission.objects.filter(student=self.request.user,
                                                                     assignment=self.object).order_by("-date")
        return context


class SubmissionCreateView(LoginRequiredMixin, View):
    form_class = SubmitAssignmentForm
    service = SubmissionService()
    template_name = "app/task_detail.html"

    def post(self, request, *args, **kwargs):
        Form = self.form_class
        form = Form(request.POST)
        if form.is_valid():
            self.service.submit_task(form, request.user, self.kwargs.get("assignment_id"))

        return redirect(reverse("assignment_detail", kwargs={"pk": self.kwargs.get("assignment_id")}))


class SubmissionDetailView(LoginRequiredMixin, DetailView):
    login_url = "/auth"
    model = AssignmentSubmission

    def get_template_names(self):
        if self.object.assignment.Type.api == self.object.assignment.assigment_type:
            if self.request.user.is_teacher():
                return ["app/submission_details_teacher.html", ]
            return ["app/submission_details_student.html"]

        if self.request.user.is_teacher():
            return ["app/submission_details_alg_teacher.html", ]
        return ["app/submission_details_alg_student.html", ]

    def _get_api_context_data(self, context, **kwargs):
        context["scenarios"] = []

        max_grade = 0
        stud_grade = 0
        for scenario in self.object.assignment.api_scenarios.all():
            to_append_scenario = {"id": scenario.id, "name": scenario.name, "steps": []}

            for step in scenario.steps.all():
                to_append_step = {"id": step.id, "name": step.name, "submission_results": [],
                                  "need_to_accordion": False}

                for validator in step.validators.all():
                    max_grade += validator.points

                    for submission_validated in validator.validated_submissions.filter(submission=self.object):
                        to_append_submission_result = {
                            "id": submission_validated,
                            "success": submission_validated.success,
                            "students_headers": submission_validated.headers,
                            "student_body": submission_validated.body,
                            "message": submission_validated.message,
                            "students_status_code": submission_validated.status,
                            "validator_allowed_response_statuses": validator.allowed_response_statuses,
                            "validator_expected_response_body": validator.expected_response_body,
                            "validator_timeout": validator.timeout
                        }
                        if submission_validated.success:
                            stud_grade += validator.points
                        else:
                            to_append_step["need_to_accordion"] = True
                        to_append_step["submission_results"].append(to_append_submission_result)
                to_append_scenario["steps"].append(to_append_step)

            context["scenarios"].append(
                to_append_scenario
            )
        context["max_grade"] = max_grade
        context["stud_grade"] = stud_grade

    def _get_alg_context_data(self, context, **kwargs):
        context["scenarios"] = []
        max_grade = 0
        stud_grade = 0

        for scenario in self.object.assignment.alg_scenarios.all():
            to_append_scenario = {"id": scenario.id, "name": scenario.name, "steps": []}

            for step in scenario.steps.all():
                submission = AlgSubmissionResults.objects.get(submission=self.object, step=step)

                to_append_step = {
                    "id": step.id,
                    "name": step.name,
                    "need_to_accordion": not submission.success,
                    "success": submission.success,
                    "actual": submission.actual,
                    "input": step.input,
                    "expected": step.expected,
                    "max_time": step.time.seconds,
                    "actual_time": submission.time.seconds
                }
                max_grade += step.points
                if submission.success:
                    stud_grade += step.points

                to_append_scenario["steps"].append(to_append_step)

            context["scenarios"].append(to_append_scenario)
        context["max_grade"] = max_grade
        context["stud_grade"] = stud_grade

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["students_name"] = f"{self.object.student.first_name} {self.object.student.last_name}"
        context["assignment_name"] = self.object.assignment.name
        if self.object.assignment.Type.api == self.object.assignment.assigment_type:
            self._get_api_context_data(context, **kwargs)
        else:
            self._get_alg_context_data(context, **kwargs)

        return context

    def get_object(self, queryset=None):
        return AssignmentSubmission.objects.filter(id=self.kwargs.get("id")) \
            .select_related("assignment", "student") \
            .prefetch_related("assignment__api_scenarios", "assignment__alg_scenarios",
                              "assignment__api_scenarios__steps",
                              "assignment__api_scenarios__steps__validators", "assignment__alg_scenarios__steps",
                              "results", "results__validator") \
            .first()
