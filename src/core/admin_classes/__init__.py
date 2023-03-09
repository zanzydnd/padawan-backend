from admin_interface.models import Theme
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from core.admin_classes.theme import CustomThemeAdmin

User = get_user_model()

# admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(Theme)

admin.site.register(Theme, CustomThemeAdmin)
