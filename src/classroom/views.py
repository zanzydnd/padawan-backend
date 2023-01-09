from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from classroom.models import Classroom
from classroom.serializers import ClassroomSerializer


class ClassroomPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == "enter_room":
            return not request.user.is_teacher()

        teacher_methods = ("POST", "PUT", "DELETE", "PATCH")
        if request.method in teacher_methods and not request.user.is_teacher():
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.user.is_teacher():
            return request.user.id == obj.teacher_id
        else:
            return Classroom.objects.filter(students__in=[request.user.id, ]).exists()


class ClassroomModelViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    permission_classes = [ClassroomPermission, IsAuthenticated]

    def get_queryset(self):
        queryset = Classroom.objects
        if self.request.user.is_teacher():
            return queryset.filter(teacher=self.request.user)
        else:
            return queryset.filter(students__in=[self.request.user, ])

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = serializer.create(validated_data=serializer.validated_data, user=request.user)
        return Response(
            status=201,
            data={
                "id": obj.id,
                "name": obj.name,
                "description": obj.description,
                "teacher_id": obj.teacher_id,
                "unique_code": obj.unique_code
            }
        )

    def get_serializer_class(self):
        if self.action == "enter_room":
            return None
        else:
            return ClassroomSerializer

    @action(
        detail=False,
        methods=['POST'],
        name='Enter Classroom by code',
        url_path="(?P<code>\w+)/enter"
    )
    def enter_room(self, request, code):
        get_object_or_404(Classroom,unique_code=code).students.add(self.request.user)
        return Response(status=200)
