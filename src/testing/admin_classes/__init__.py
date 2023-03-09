from django.contrib import admin

from testing.admin_classes.scenario import ScenarioAdmin
from testing.models import Scenario

admin.site.register(Scenario, ScenarioAdmin)
