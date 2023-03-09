from django.apps import apps
from django.contrib import admin
from django.urls import reverse, NoReverseMatch
from django.utils.text import capfirst


class CustomAdminSite(admin.AdminSite):
    def _build_app_dict(self, request, label=None):
        app_dict = {}

        if label:
            models = {
                m: m_a for m, m_a in self._registry.items()
                if m._meta.app_label == label
            }
        else:
            models = self._registry

        for model, model_admin in models.items():
            app_label = model._meta.app_label

            has_module_perms = model_admin.has_module_permission(request)
            if not has_module_perms:
                continue

            perms = model_admin.get_model_perms(request)
            if True not in perms.values():
                continue

            info = (app_label, model._meta.model_name)
            model_dict = {
                "name": capfirst(model._meta.verbose_name_plural),
                "tooltip_description": model.tooltip_description if hasattr(model, "tooltip_description") else "",
                "object_name": model._meta.object_name,
                "perms": perms,
                "admin_url": None,
                "add_url": None
            }

            if perms.get("change") or perms.get("view"):
                model_dict["view_only"] = not perms.get("change")
                try:
                    model_dict["admin_url"] = reverse("admin:%s_%s_changelist" % info, current_app=self.name)
                except NoReverseMatch:
                    pass

            if perms.get("add"):
                try:
                    model_dict["add_url"] = reverse("admin:%s_%s_add" % info, current_app=self.name)
                except NoReverseMatch:
                    pass

            if app_label in app_dict:
                app_dict[app_label]["models"].append(model_dict)
            else:
                app = apps.get_app_config(app_label)
                app_dict[app_label] = {
                    "name": app.verbose_name,
                    "tooltip_description": app.tooltip_description if hasattr(app, "tooltip_description") else "",
                    "app_label": app_label,
                    "app_url": reverse(
                        "admin:app_list",
                        kwargs={"app_label": app_label},
                        current_app=self.name
                    ),
                    "has_module_perms": has_module_perms,
                    "models": [model_dict],
                }

        if label:
            return app_dict.get(label)
        return app_dict

    def get_app_list(self, request, app_label=None):
        app_dict = self._build_app_dict(request)

        app_list = []
        app_list.append(app_dict.get("assigment"))
        app_list.append(app_dict.get("classroom"))
        app_list.append(app_dict.get("testing"))

        for item in app_dict.values():
            if item in app_list:
                continue
            app_list.append(item)

        return list(filter(lambda x: x is not None, app_list))
