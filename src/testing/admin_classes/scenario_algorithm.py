from nested_admin.nested import NestedModelAdmin, NestedStackedInline

from testing.models import AlgScenarioStep


class StepSortableInline(NestedStackedInline):
    model = AlgScenarioStep
    extra = 0
    classes = ["wide", ]
    fields = ("input", "expected", "time", "points")


class AlgScenarioAdmin(NestedModelAdmin):
    inlines = (StepSortableInline,)
