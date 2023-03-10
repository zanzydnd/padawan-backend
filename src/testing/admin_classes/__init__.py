from django.contrib import admin

from testing.admin_classes.scenario import ScenarioAdmin
from testing.admin_classes.scenario_algorithm import AlgScenarioAdmin
from testing.models import Scenario, AlgScenario

admin.site.register(Scenario, ScenarioAdmin)
admin.site.register(AlgScenario, AlgScenarioAdmin)
