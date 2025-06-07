import random

from constant import BASE_URL, HEADERS


class TestBookings:


    def test_create_booking(self, booking_data, auth_session):
        create_booking = auth_session.post(f"{BASE_URL}/booking", json=booking_data)
        assert create_booking.status_code == 200
        booking_id = create_booking.json().get("bookingid")
        assert booking_id is not None, "ID букинга не найден в ответе"

        get_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_booking.status_code == 200

        booking_data_response = get_booking.json()
        assert booking_data_response['firstname'] == booking_data['firstname'], "Имя не совпадает с заданным"
        assert booking_data_response['lastname'] == booking_data['lastname'], "Фамилия не совпадает с заданной"
        assert booking_data_response['totalprice'] == booking_data['totalprice'], "Цена не совпадает с заданной"
        assert booking_data_response['depositpaid'] == booking_data['depositpaid'], "Статус депозита не совпадает"
        assert booking_data_response['bookingdates']['checkin'] == booking_data['bookingdates'][
            'checkin'], "Дата заезда не совпадает"
        assert booking_data_response['bookingdates']['checkout'] == booking_data['bookingdates'][
            'checkout'], "Дата выезда не совпадает"

        delete_booking = auth_session.delete(f"{BASE_URL}/booking/{booking_id}")
        assert delete_booking.status_code == 201, f"Ошибка при удалении букинга с ID {booking_id}"

        get_deleted_booking = auth_session.get(f"{BASE_URL}/booking/{booking_id}")
        assert get_deleted_booking.status_code == 404, "Букинг не был удален"


# 1 pozitive получение списка броней
    def test_get_booking(self, auth_session):
        get_booking = auth_session.get(f"{BASE_URL}/booking")
        assert get_booking.status_code == 200

        booking_data_response = get_booking.json()
        assert type(booking_data_response) is list, "Сервер возвращает не список"

        number = all(isinstance(item["bookingid"], int) for item in booking_data_response)
        assert number, "Не все bookingid являются целыми числами"


# 2 pozitive обновление брони с id
    def test_update_booking(self, booking_data, auth_session, random_booking_id):
        update_booking = auth_session.put(f"{BASE_URL}/booking/{random_booking_id}", json=booking_data)
        assert update_booking.status_code == 200

        get_booking_id_up = auth_session.get(f"{BASE_URL}/booking/{random_booking_id}")
        assert get_booking_id_up.status_code == 200

        booking_data_response = get_booking_id_up.json()
        assert booking_data_response['firstname'] == booking_data['firstname'], "Имя не совпадает с заданным"
        assert booking_data_response['lastname'] == booking_data['lastname'], "Фамилия не совпадает с заданной"
        assert booking_data_response['totalprice'] == booking_data['totalprice'], "Цена не совпадает с заданной"
        assert booking_data_response['depositpaid'] == booking_data['depositpaid'], "Статус депозита не совпадает"
        assert booking_data_response['bookingdates']['checkin'] == booking_data['bookingdates'][
            'checkin'], "Дата заезда не совпадает"
        assert booking_data_response['bookingdates']['checkout'] == booking_data['bookingdates'][
            'checkout'], "Дата выезда не совпадает"

# 3 negative обновление несуществующей брони
    def test_update_none_booking(self, booking_data, auth_session):
        get_booking = auth_session.get(f"{BASE_URL}/booking").json()
        booking_id = [item["bookingid"] for item in get_booking]
        none_ids = [x for x in range(1, 10000) if x not in booking_id]
        none_booking_id = random.choice(none_ids)
        update_booking = auth_session.put(f"{BASE_URL}/booking/{none_booking_id}", json=booking_data)
        assert update_booking.status_code == 405, "Сервер готов обновлять несуществующую бронь"


# 4 negative без токена
    def test_update_none_token(self, booking_data, auth_session, random_booking_id):
        update_booking = auth_session.put(f"{BASE_URL}/booking/{random_booking_id}", headers={"Cookie": "token"}, json=booking_data)
        assert update_booking.status_code == 403, "Сервер предоставляет права сверх авторизации"


# 5 negative неверное тело запроса
    def test_update_booking_body(self, booking_data, auth_session, random_booking_id):
        update_booking = auth_session.put(f"{BASE_URL}/booking/{random_booking_id}", json=booking_data.pop("totalprice"))
        assert update_booking.status_code == 400, "Сервер принимает запрос с неправильным телом"


# 8 pozitive обновление поля брони с id
    def test_part_update_booking(self, booking_data_prsn, auth_session, random_booking_id):
        update_booking = auth_session.patch(f"{BASE_URL}/booking/{random_booking_id}", json=booking_data_prsn)
        assert update_booking.status_code == 200

        get_booking_id_up = auth_session.get(f"{BASE_URL}/booking/{random_booking_id}")
        assert get_booking_id_up.status_code == 200

        booking_data_response = get_booking_id_up.json()
        assert booking_data_response['firstname'] == booking_data_prsn['firstname'], "Имя не совпадает с заданным"
        assert booking_data_response['lastname'] == booking_data_prsn['lastname'], "Фамилия не совпадает с заданной"

# 16 negative цена <= 0
    def test_low_price(self, booking_data_prsn, auth_session, random_booking_id):
        update_booking = auth_session.patch(f"{BASE_URL}/booking/{random_booking_id}", json={"totalprice": -1})
        assert update_booking.status_code == 400, "Установлена стоимость нуль или ниже!"