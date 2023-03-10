from django.contrib import admin

from assignment.models import Assignment, AssignmentSubmission
from testing.models import Scenario, AlgScenario


class AssignmentAdmin(admin.ModelAdmin):
    db_model = Assignment
    list_max_show_all = 100
    default_fields = ["name", "description", "assigment_type", "max_points", "one_try", "task_file", ]

    def get_form(self, request, obj=None, change=False, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)

        if obj:
            if obj.assigment_type == Assignment.Type.api:
                form.base_fields["api_scenarios"].queryset = Scenario.objects.all()
            else:
                form.base_fields["alg_scenarios"].queryset = AlgScenario.objects.all()
        return form

    def get_fields(self, request, obj=None):
        if obj:
            if obj.assigment_type == Assignment.Type.api:
                return self.default_fields + ["api_scenarios", ]
            return self.default_fields + ["alg_scenarios", ]
        return self.default_fields


class SubmissionAdmin(admin.ModelAdmin):
    model = AssignmentSubmission
    list_max_show_all = 100
