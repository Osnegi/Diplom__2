import pytest
import allure
from api_helper import user_registration, delete_user

class TestUserRegistration:

    @allure.title('Регистрируем уникального пользователя - позитивная проверка')
    def test_create_new_user_positive_check(self, new_user):

        response = user_registration(new_user)

        assert response.status_code == 200
        assert response.json()['success'] == True

        assert response.json()['user']['name'] == new_user['name']
        assert response.json()['user']['email'] == new_user['email']

        assert  response.json()['accessToken'] != ''
        assert  response.json()['refreshToken'] != ''

        delete_user(response.json()['accessToken'])

    @allure.title('Пытаемся зарегистрировать уже существующего пользователя - негативная проверка')
    def test_create_existed_user_negative_check(self, new_user):

        response_unique = user_registration(new_user)
        response_double = user_registration(new_user)

        delete_user(response_unique.json()['accessToken'])

        assert response_double.status_code == 403
        assert response_double.json()['success'] == False
        assert response_double.json()['message'] == 'User with such email already exists'

    @allure.title('Пытаемся зарегистрировать пользователя с одним из пустых полей - негативна проверка')
    @pytest.mark.parametrize('empty_input', ['name', 'email', 'password'])
    def test_create_user_empty_input_negative_check(self, new_user, empty_input):

        del new_user[empty_input]
        response = user_registration(new_user)

        assert response.status_code == 403
        assert response.json()['success'] == False
        assert response.json()['message'] == 'Email, password and name are required fields'