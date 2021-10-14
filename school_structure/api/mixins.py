class MixinSerializer:
    def get_serializer_class(self):
        try:
            serializer_class = self.serializer_class_by_action[self.action]
        except KeyError:
            serializer_class = self.serializer_class
        return serializer_class


class MixinPermissions:
    def get_permissions(self):
        try:
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            return [permission() for permission in self.permission_classes]


class MixedPermissionSerializer(MixinPermissions, MixinSerializer):
    pass
