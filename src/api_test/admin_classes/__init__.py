from django.contrib import admin

from api_test.admin_classes.scenario import ScenarioAdmin
from api_test.models import Scenario

admin.site.register(Scenario, ScenarioAdmin)
