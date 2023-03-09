from django.contrib import admin


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
