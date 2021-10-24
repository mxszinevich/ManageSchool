from rest_framework import permissions

from users.models import StaffUser

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')


class StaffUserPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            if view.action == 'list' and request.user.is_authenticated:
                return True
            elif view.action in ['create', 'update', 'destroy'] \
                    and (request.user.is_staff or request.user.staff.position in [
                StaffUser.POSITION_DIRECTOR,
                StaffUser.POSITION_ADMINISTRATOR,
            ]):
                return True

        except AttributeError:
            return False

        return False

    def has_object_permission(self, request, view, obj):
        try:
            if request.user.is_staff or request.user.staff.position in [
                StaffUser.POSITION_DIRECTOR,
                StaffUser.POSITION_ADMINISTRATOR,
            ]:
                return True
            else:
                return False
        except AttributeError:
            return False


class StudentUserPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            if request.user.is_staff or request.user.staff:  # Могут просматривать, изменять и создавать только сотрудники
                return True
        except AttributeError:
            return False


class StudentInfoPermissions(permissions.BasePermission):
    """Сведения о ученике могут просматривать сотрудники и сам ученик"""
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        user = request.user
        try:
            if user.is_staff or getattr(user, 'student', False):
                if user.student == obj:
                    return True
            elif user.is_staff or getattr(user, 'staff', False):
                return True
            return False
        except AttributeError:
            return False
