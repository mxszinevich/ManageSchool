class MixinSerializer:
    def get_serializer_class(self):
        try:
            serializer_class = self.serializer_class_by_action[self.action]
        except KeyError:
            serializer_class = self.serializer_class
        return serializer_class
