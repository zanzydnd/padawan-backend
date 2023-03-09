from django.contrib import admin

from assignment.admin_classes.assignment import AssignmentAdmin, SubmissionAdmin
from assignment.models import Assignment, AssignmentSubmission

admin.site.register(Assignment, AssignmentAdmin)
admin.site.register(AssignmentSubmission, SubmissionAdmin)
