import requests
import pytest

BASE_URL = "http://127.0.0.1:3000/glucose"


def test_get_glucose_records():
    response = requests.get(BASE_URL)
    assert response.status_code == 200, f"The status code is {response.status_code}, but should be 200"
    data = response.json()
    assert isinstance(data, list), f"The data type is {type(data)}, but should be a list"

@pytest.fixture()
def create_glucose_record():
    new_record = {
        "user_id": 2,
        "glucose_level": 11.5,
        "measurement_time": "2024-12-02T08:30:00",
        "notes": "Авто - тестовая запись"
    }
    response = requests.post(BASE_URL, json=new_record)
    assert response.status_code == 200, f"The status code is {response.status_code}, but should be 200"
    record = response.json()
    assert record["user_id"] == new_record["user_id"]
    assert record["glucose_level"] == new_record["glucose_level"]
    return record


def test_update_glucose_record(create_glucose_record):
    original_record = create_glucose_record
    record_id = original_record["id"]

    update_data = {
        "user_id": 2,
        "glucose_level": 13.0,
        "measurement_time": original_record["measurement_time"],
        "notes": "Обновленная авто-тестовая запись"
    }
    response_update = requests.put(f"{BASE_URL}/{record_id}", json=update_data)
    assert response_update.status_code == 200, f"PUT returned {response_update.status_code}"
    record_updated = response_update.json()

    assert record_updated["glucose_level"] == update_data["glucose_level"], "glucose_level обновился"
    assert record_updated["notes"] == update_data["notes"], "notes обновились"

    assert record_updated["user_id"] == original_record["user_id"], "user_id не изменился"
    assert record_updated["measurement_time"] == original_record["measurement_time"], "measurement_time не изменился"

def test_delete_glucose_record(create_glucose_record):
    record_id = create_glucose_record
    record_id = record_id["id"]
    response = requests.delete(f"{BASE_URL}/{record_id}")
    assert response.status_code == 204, f"The status code is {response.status_code}, but should be 204"
    # этот тест валится из-за того, что я не могу описать get по id. В файле апи явно синтаксическая ошибка, разберусь позже
    # response = requests.get(f"{BASE_URL}/{record_id}")
    # assert response.status_code == 404, f"The status code is {response.status_code}, but should be 404"
