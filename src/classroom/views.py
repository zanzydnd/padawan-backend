from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination

from classroom.models import Classroom
from classroom.serializers import ClassroomSerializer


class ClassroomModelViewSet(viewsets.ModelViewSet):
    pagination_class = PageNumberPagination
    serializer_class = ClassroomSerializer

    def get_queryset(self):
        queryset = Classroom.objects
        if self.request.user.is_teacher():
            return queryset.filter(teacher=self.request.user)
        else:
            return queryset.filter(students__in=[self.request.user,])

    @action(detail=False, methods=['POST'], name='Enter Classroom by code',
            url_path="(?P<code>\w+)/enter")
    def enter_room(self):
        pass
