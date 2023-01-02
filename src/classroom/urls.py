from rest_framework import routers

from classroom.views import ClassroomModelViewSet

classroom_router = routers.SimpleRouter()
classroom_router.register("classroom", ClassroomModelViewSet, basename="Classroom")
urlpatterns = [
    *classroom_router.urls
]
