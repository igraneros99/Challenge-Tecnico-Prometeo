import pytest
import requests
import allure
import json
from env import credentials

URL = credentials["BASE_URL"]
API_KEY = credentials["API_KEY"]

HEADERS = {
    "accept": "application/json",
    "content-type": "application/x-www-form-urlencoded",
    "X-API-Key": API_KEY,
}

flaky_cases = [
    pytest.param(
        {"account_number": "1002", "branch_code": "00001", "bank_code": "999", "country_code": "BR", "document_number": "58.547.642/0001-95", "account_type": "CHECKING"},
        404,
        {"data.valid": False, "errors.message": "Cuenta credito invalida"},
        id="BR Invalid account"
    ),
    pytest.param(
        {"account_number": "BR3899999999010100000001002C1", "country_code": "BR", "document_number": "58.547.642/0001-95"},
        404,
        {"data.valid": False, "errors.message": "Cuenta credito invalida"},
        id="Br invalid IBAN"
    ),
]

@allure.feature("BR Account Validation")
@allure.story("Flaky testcases")
@pytest.mark.parametrize("payload, expected_status, expected_fields", flaky_cases)
def test_brazil_flaky(payload, expected_status, expected_fields):
    response = requests.post(URL, headers=HEADERS, data=payload, timeout=10)

    try:
        response_json = response.json()
    except ValueError:
        response_json = {}

    allure.attach(
        json.dumps(response_json, indent=2, ensure_ascii=False),
        name="response.json",
        attachment_type=allure.attachment_type.JSON
    )

    if expected_status is not None:
        assert response.status_code == expected_status

    for field, expected_value in expected_fields.items():
        keys = field.split(".")
        value = response_json
        for k in keys:
            value = value.get(k, {})
        assert value == expected_value
