import pytest
import requests
import allure
import urls
from data import DataMessages

class TestLoginUser:

    @allure.title('Авторизуем (логиним) зарегистрированного пользователя - позитивная проверка')
    def test_login_user_positive_check(self, client):

        response = requests.post(urls.BASE_URL + urls.LOGIN_USER_ENDPOINT, data = client[0])

        assert response.status_code == 200
        assert response.json()['success'] == True

        assert response.json()['accessToken'] != ''
        assert response.json()['refreshToken'] != ''

        assert response.json()['user']['name'] == client[0]['name']
        assert response.json()['user']['email'] == client[0]['email']

    @allure.title('Авторизуем пользователя с ошибкой в логине или пароле - негативная проверка')
    @pytest.mark.parametrize('mistake_field', ['email', 'password'])
    def test_login_user_negative_check(self, client, mistake_field):

        client[0][mistake_field] = client[0][mistake_field] + '1'
        response = requests.post(urls.BASE_URL + urls.LOGIN_USER_ENDPOINT, data = client[0])

        assert response.status_code == 401
        assert response.json()['success'] == False
        assert response.json()['message'] == DataMessages.INCORRECT_LOGIN_DATA