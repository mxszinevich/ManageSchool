from rest_framework.permissions import BasePermission
from users.models import StaffUser


class SchoolBaseAdministrationPermissions(BasePermission):
    """Разрешения для администрирования(управления) школой"""
    def has_permission(self, request, view):
        try:
            if request.user.is_staff or request.user.staff.position in [
                StaffUser.POSITION_ADMINISTRATOR,
                StaffUser.POSITION_DIRECTOR
            ]:
                return True
            return False
        except AttributeError:
            return False


class SchoolStaffPermissions(BasePermission):
    """Разрещения для просмотра и управления пользовательскими данными"""
    def has_permission(self, request, view):
        try:
            if request.user.is_staff or request.user.staff:
                return True
            return False
        except AttributeError:
            return False

    def has_object_permission(self, request, view, obj):
        # @TODO добавить зависимость действий учителя от студента
        return True




