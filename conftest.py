import pytest
from helper import RandomUserData
from api_helper import delete_user, create_new_order, user_registration

@pytest.fixture(scope = 'function')
def new_user():
    user_data_generator = RandomUserData()
    user_data = user_data_generator.user_data_generation()
    return user_data

@pytest.fixture(scope = 'function')
def client(new_user):
    response = user_registration(new_user)
    access_token = response.json()['accessToken']
    yield new_user, access_token
    delete_user(access_token)

@pytest.fixture(scope = 'function')
def order(client):
    user_data, access_token = client
    for i in range(3):
        create_new_order(access_token)