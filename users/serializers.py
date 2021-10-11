from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        tokens_data = super().validate(attrs)
        if not self.user.is_account_confirmation:
            raise PermissionDenied('Аккаунт не подтвержден. Обратитесь к администратору')
        return tokens_data
