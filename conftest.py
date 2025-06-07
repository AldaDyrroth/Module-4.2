import requests
import pytest
import random
from constant import HEADERS, BASE_URL
from faker import Faker
faker = Faker()

@pytest.fixture(scope="session")
def auth_session():
    """Создаёт сессию с авторизацией и возвращает объект сессии."""
    session = requests.Session()
    session.headers.update(HEADERS)

    auth_response = session.post(f"{BASE_URL}/auth", json={"username": "admin", "password": "password123"})
    assert auth_response.status_code == 200, "Ошибка авторизации, статус код не 200"

    token = auth_response.json().get("token")
    assert token is not None, "Токен не найден в ответе"

    session.headers.update({"Cookie": f"token={token}"})
    return session

@pytest.fixture(scope="session")
def booking_data():
    return {
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
        "totalprice": faker.random_int(min=100, max=10000),
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2024-04-05",
            "checkout": "2024-04-08"
        },
        "additionalneeds": "Breakfast"
    }

@pytest.fixture()
def random_booking_id():
    session = requests.Session()
    response = session.get(f"{BASE_URL}/booking")
    assert response.status_code == 200, "Ошибка авторизации, статус код не 200"

    get_booking = response.json()
    id = random.choice(get_booking)["bookingid"]
    return id

@pytest.fixture()
def booking_data_prsn():
    return {
        "firstname": faker.first_name(),
        "lastname": faker.last_name(),
    }
