import requests
import allure
import urls
from api_helper import create_list_ingredients
from data import DataMessages

class TestCreateOrder:

    @allure.title('Создаем заказ авторизованным пользователем - позитивная проверка')
    def test_create_order_authorised_user_positive_check(self, client):

        user_data, access_token = client

        order = {'ingredients': create_list_ingredients()}
        response = requests.post(urls.BASE_URL + urls.ORDERS_ENDPOINT, headers = {'Authorization': access_token}, data = order)

        assert response.status_code == 200
        assert response.json()['name'] != ''
        assert response.json()['order']['number'] != ''
        assert response.json()['success'] == True

    @allure.title('Создаем заказ неавторизованным пользователем (гостем) - позитивная проверка')
    def test_create_order_unauthorised_user_positive_check(self):

        order = {'ingredients': create_list_ingredients()}
        response = requests.post(urls.BASE_URL + urls.ORDERS_ENDPOINT, data = order)

        assert response.status_code == 200
        assert response.json()['name'] != ''
        assert response.json()['order']['number'] != ''
        assert response.json()['success'] == True

    @allure.title('Создаем заказ без ингредиентов - негативная проверка')
    def test_create_order_empty_ingredients_list_negative_check(self):

        order = {'ingredients': []}
        response = requests.post(urls.BASE_URL + urls.ORDERS_ENDPOINT, data = order)

        assert response.status_code == 400
        assert response.json()['success'] == False
        assert response.json()['message'] == DataMessages.CREATE_ORDER_EMPTY_INGREDIENTS

    @allure.title('Создаем заказ с неверным хешем ингредиентов - негативная проверка')
    def test_create_order_false_hash_ingredients_negative_check(self):

        order = {'ingredients': ['abracadabra100', 'superkalifragiristikexpialidoshes']}
        response = requests.post(urls.BASE_URL + urls.ORDERS_ENDPOINT, data = order)

        assert response.status_code == 500