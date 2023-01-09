from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import BasePermission
from rest_framework.response import Response

from api.serializers import UserCreateSerializer, UserSerializer

User = get_user_model()


class UserApiViewPermission(BasePermission):
    def has_permission(self, request, view):
        if view.action == "current_user" and not request.user.is_authenticated:
            return False
        if view.action == "create" and request.user.is_authenticated:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id


class UserApiViewModelSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [UserApiViewPermission]

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    @action(detail=False, methods=['GET'], name='Get Current User', url_path="info")
    def current_user(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user, many=False)
        return Response(serializer.data)
