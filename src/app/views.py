from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView, DetailView, ListView

from assignment.models import Assignment
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
