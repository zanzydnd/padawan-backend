from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from api.serializers import UserCreateSerializer, UserSerializer

User = get_user_model()


class UserApiViewModelSet(viewsets.ModelViewSet):
    queryset = User.objects.all().prefetch_related('images')
    pagination_class = PageNumberPagination

    def get_serializer_class(self):
        if self.action == 'create':
            return UserCreateSerializer
        return UserSerializer

    @action(detail=False, methods=['GET'], name='Get Current User', url_path="info")
    def current_user(self, request, *args, **kwargs):
        if not request.auth:
            raise PermissionDenied(detail="Аутенфицируйтесь.")

        token = Token.objects.get(key=request.auth)

        user = User.objects.get(id=token.user_id)

        serializer = self.get_serializer(user, many=False)
        return Response(serializer.data)
