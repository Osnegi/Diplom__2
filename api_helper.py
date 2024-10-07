import requests
import urls
import allure

@allure.step('Регистрируем нового пользователя')
def user_registration(user_data):
    response = requests.post(urls.BASE_URL + urls.REGISTRATION_USER_ENDPOINT, data = user_data)
    return response

@allure.step('Формируем перечень ингредиентов для оформления заказа')
def create_list_ingredients():

    response = requests.get(urls.BASE_URL + urls.INGREDIENTS_ENDPOINT)
    ingredient1 = response.json()['data'][0]['_id']
    ingredient2 = response.json()['data'][7]['_id']
    ingredient3 = response.json()['data'][10]['_id']

    list_ingredients = []
    list_ingredients.append(ingredient1)
    list_ingredients.append(ingredient2)
    list_ingredients.append(ingredient3)

    return list_ingredients

@allure.step('Удаляем зарегистрированного пользователя')
def delete_user(access_token):
    requests.delete(urls.BASE_URL + urls.USER_DATA_ENDPOINT, headers = {'Authorization': access_token})

@allure.step('Оформляем заказ авторизованного пользователя')
def create_new_order(access_token):
    order = {}
    order['ingredients'] = create_list_ingredients()
    response = requests.post(urls.BASE_URL + urls.ORDERS_ENDPOINT, headers = {'Authorization': access_token}, data = order)

    return response
