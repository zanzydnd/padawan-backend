from pprint import pprint

from adminsortable2.admin import SortableInlineAdminMixin
from django import forms
from django.contrib import admin, messages
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import path, reverse
from django.forms import ValidationError
from nested_admin.nested import NestedModelAdmin, NestedTabularInline, NestedStackedInline

from padawan.exceptions import ImportingFileException, ScenarioValidationError
from api_test.models import Step, Scenario, ScenarioConfig, StepValidator
from api_test.utils import imported_file_to_dict, scenario_dict_to_scenario_db, scenario_db_to_dict, \
    validate_imported_scenario_dict
from padawan.forms import ImportFileForm


class StepValidatorNestedTabularInline(NestedTabularInline):
    model = StepValidator
    extra = 0
    classes = ["label", "wide"]


class StepSortableInline(NestedStackedInline):
    model = Step
    inlines = (StepValidatorNestedTabularInline,)
    extra = 0
    fields = ["name", "url", "method", "body", "headers"]
    classes = ["wide", ]


class JsonYamlImportFileForm(ImportFileForm):
    def clean_file(self):
        file = self.cleaned_data.get("file")

        if not file.name.endswith('.yaml') and file.name.endswith('.json') and not file.name.endswith('.yml'):
            raise forms.ValidationError("Поддерживается только json, yml, yaml.")

        return file


class ScenarioAdmin(NestedModelAdmin):
    inlines = (StepSortableInline,)
    change_list_template = "admin/scenario/changelist.html"
    change_form_template = "admin/scenario/change_form.html"

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('import-scenario/', self.import_scenario),
        ]
        return my_urls + urls

    def save_formset(self, request, form, formset, change):
        try:
            with transaction.atomic():
                formset.save()
                form.instance.save()

                validate_imported_scenario_dict(scenario_db_to_dict(form.instance))
        except ScenarioValidationError as e:
            messages.error(request, e)

    def save_model(self, request, obj, form, change):
        pass

    def import_scenario(self, request):
        if request.method == "POST":
            try:
                scenario_dict = imported_file_to_dict(request.FILES["file"])
                scenario, list_of_steps = scenario_dict_to_scenario_db(scenario_dict)
                Step.objects.bulk_create(list_of_steps)
                return HttpResponseRedirect(
                    reverse("admin:api_test_scenario_change", kwargs={"object_id": scenario.id}))
            except ImportingFileException as e:
                messages.error(request, e)
        form = ImportFileForm()
        form.base_fields['file'].help_text = "Поддерживается только yaml, json."
        payload = {"form": form}
        return render(
            request, "admin/fileform.html", payload
        )
