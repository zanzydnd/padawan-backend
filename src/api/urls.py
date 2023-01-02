from django.urls import re_path, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers

from api.views import UserApiViewModelSet
from rest_framework.authtoken import views as auth_views
from classroom.urls import urlpatterns as classroom_urls

schema_view = get_schema_view(
    openapi.Info(
        title="Referal API",
        default_version="v1",
        description="PADAWAN BACKEND API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="zanzydnd@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)

user_router = routers.SimpleRouter()
user_router.register("user", UserApiViewModelSet, basename="User")

urlpatterns = [
    *user_router.urls,
    *classroom_urls,
    path("auth/", auth_views.obtain_auth_token),
    re_path("swagger(?P<format>\.json|\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
