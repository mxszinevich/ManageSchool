from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User, StaffUser
from users.tests.tests_data.data import (
    test_user_data,
    test_superuser_data,
    test_user_create_data,
)


class BaseTestCase(APITestCase):
    def setUp(self):
        self.url_token_create = reverse('token_create')

        self.test_superuser = User.objects.create_superuser(**test_superuser_data)
        self.test_user = User.objects.create_user(**test_user_data)

    def get_access_token(self, *, email, password):
        """Получение jwt-токена"""
        response = self.client.post(self.url_token_create, {'email': email, 'password': password})
        return response.data.get('access')

    def request(self, method, url, data={}, auth=True, superuser=True):
        """Метод выполнения запросов"""
        if superuser:
            access_token = self.get_access_token(email=test_superuser_data['email'],
                                                 password=test_superuser_data['password'],
                                                 )
        else:
            access_token = self.get_access_token(email=test_user_data['email'],
                                                 password=test_user_data['password'],
                                                 )
        if auth:
            if access_token:
                self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        return method(url, data)

    def test_superuser_auth(self):
        """Авторизация superuser"""
        response = self.request(self.client.post, self.url_token_create, test_superuser_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_auth_permission_denied(self):
        """Авторизация пользователя без подтверждения"""
        response = self.request(self.client.post, self.url_token_create,  test_user_data, superuser=False)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_auth(self):
        """Авторизация пользователя c подтверждением"""
        self.test_user.is_account_confirmation = True
        self.test_superuser.save(update_fields=['is_account_confirmation'])
        response = self.request(self.client.post, self.url_token_create, test_user_data, superuser=False)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class StudentsListView(BaseTestCase):
    """Тестирование работы со студентами"""

    def setUp(self):
        super(StudentsListView, self).setUp()
        self.url_students_list = '/api/users/students'

    def test_get_students_list_unauthorized(self):
        """Получение списка студентов неавторизованным пользователем"""
        response = self.request(self.client.get, self.url_students_list, auth=False)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_students_list_superuser(self):
        """Получение списка студентов superuser"""
        response = self.request(self.client.get, self.url_students_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_students_list_staff(self):
        """Получение списка студентов подтвержденным сотрудником школы"""
        self.test_user.is_account_confirmation = True
        self.test_user.save(update_fields=['is_account_confirmation'])
        staff = StaffUser.objects.create(user=self.test_user, position=1)
        response = self.request(self.client.get, self.url_students_list, superuser=False)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_students_list_staff(self):
        """Получение списка студентов неподтвержденным сотрудником школы"""
        staff = StaffUser.objects.create(user=self.test_user, position=1)
        response = self.request(self.client.get, self.url_students_list, superuser=False)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
