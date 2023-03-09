from django.contrib import admin

from assignment.models import Assignment, AssignmentSubmission


class AssignmentAdmin(admin.ModelAdmin):
    db_model = Assignment
    list_max_show_all = 100


class SubmissionAdmin(admin.ModelAdmin):
    model = AssignmentSubmission
    list_max_show_all = 100