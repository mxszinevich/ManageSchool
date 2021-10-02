from rest_framework import permissions

# @TODO Как работет
class MixedPermission:
    """ Permissions action`s mixin
    """
    def get_permissions(self):
        try:
            return [permission_classes() for permission_classes in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission_classes() for permission_classes in self.permission_classes]

class EducationClassesPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    # def has_object_permission(self, request, view, obj):
    #     if obj.author == request.user:
    #         return True
    #     return False