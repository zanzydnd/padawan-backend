from rest_framework.permissions import BasePermission


class TeacherPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_teacher


class StudentPermission(BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_teacher

