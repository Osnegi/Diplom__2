import requests
import allure
import urls
from data import DataMessages

class TestGetUserOrder:

    @allure.title('Получаем заказы авторизованного пользователя - негативная проверка')

    def test_get_authorised_user_orders_positive_check(self, client, order):

        user_data, access_token = client
        response = requests.get(urls.BASE_URL + urls.ORDERS_ENDPOINT, headers = {'Authorization': access_token})

        assert response.status_code == 200
        assert response.json()['success'] == True

        assert len(response.json()['orders']) == 3
        assert response.json()['total'] != 0
        assert response.json()['totalToday'] != 0

    @allure.title('Получаем заказы неавторизованного пользователя (гостя) - негативная проверка')
    def test_get_unauthorised_user_orders_negative_check(self, order):

        response = requests.get(urls.BASE_URL + urls.ORDERS_ENDPOINT)

        assert response.status_code == 401
        assert response.json()['success'] == False
        assert response.json()['message'] == DataMessages.UNAUTHORISED_USER