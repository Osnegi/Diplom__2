import pytest
import requests
import allure
import urls
from helper import RandomUserData
from data import DataMessages


class TestChangeUserData:

    @allure.title('Меняем данные пользователя с авторизацией (имя или почту) - позитивная проверка')
    @pytest.mark.parametrize('new_field', ['name', 'email'])
    def test_change_authorised_user_data_name_or_email_positive_check(self, client, new_field):
        user_data, access_token = client

        user_data_generator = RandomUserData()
        new_user_data = user_data_generator.user_data_generation()

        user_data[new_field] = new_user_data[new_field]
        response = requests.patch(urls.BASE_URL + urls.USER_DATA_ENDPOINT, headers={'Authorization': access_token},
                                  data=user_data)

        assert response.status_code == 200
        assert response.json()['success']
        assert response.json()['user']['name'] != ''
        assert response.json()['user']['email'] != ''
        assert response.json()['user'][new_field] == new_user_data[new_field]

    @allure.title('Меняем данные пользователя с авторизацией (пароль) - позитивная проверка')
    def test_change_authorised_user_data_password_positive_check(self, client):
        user_data, access_token = client

        user_data_generator = RandomUserData()
        new_user_data = user_data_generator.user_data_generation()

        user_data['password'] = new_user_data['password']
        response = requests.patch(urls.BASE_URL + urls.USER_DATA_ENDPOINT, headers={'Authorization': access_token},
                                  data=user_data)

        assert response.status_code == 200
        assert response.json()['success'] == True
        assert response.json()['user']['name'] != ''
        assert response.json()['user']['email'] != ''

    @allure.title('Меняем данные пользователя без авторизации - негативная проверка')
    @pytest.mark.parametrize('new_field', ['name', 'email', 'password'])
    def test_change_unauthorised_user_data_negative_check(self, client, new_field):
        user_data, access_token = client

        user_data_generator = RandomUserData()
        new_data = user_data_generator.user_data_generation()

        user_data[new_field] = new_data[new_field]
        response = requests.patch(urls.BASE_URL + urls.USER_DATA_ENDPOINT, data=user_data)

        assert response.status_code == 401
        assert response.json()['success'] == False
        assert response.json()['message'] == DataMessages.UNAUTHORISED_USER
