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

test_cases = [
    pytest.param(
        {"account_number": "9990000100000000000000", "country_code": "AR", "document_number": "30-71515454-1"},
        200,
        {"data.valid": True, "data.beneficiary_name": "ROBERTO CARLOS"},
        id="AR valid account"
    ),
    pytest.param(
        {"account_number": "abcd1234", "country_code": "AR", "document_number": "30-71515454-1"},
        None,
        {},
        marks=pytest.mark.xfail(reason="Sandbox puede dar 500"),
        id="AR malformed account number (sandbox bug)"
    ),
    pytest.param(
        {"country_code": "AR", "document_number": "30-71515454-1"},
        400,
        {"errors.message": "Missing parameter: account_number"},
        id="AR missing account number"
    ),
    pytest.param(
        {"account_number": "0720000300000001354934", "document_number": "30-71515454-1"},
        400,
        {"errors.code": 400, "errors.message": "Missing parameter: country_code"},
        id="AR missing country code"
    ),
    pytest.param(
        {"account_number": "prometeo.pruebas.mp", "country_code": "AR"},
        200,
        {
            "data.valid": True,
            "data.beneficiary_name": "ROBERTO CARLOS",
            "data.account_type": "CHECKING",
            "data.account_currency": "ARS"
        },
        id="AR alias valid"
    ),
    pytest.param(
        {"account_number": "prometeofallo.pruebas.mp", "country_code": "AR"},
        500,
        {"errors.code": 500, "errors.message": "Error interno"},
        marks=pytest.mark.xfail(reason="Sandbox devuelve 500 por alias inválido, debería ser 404"),
        id="AR alias invalid (sandbox bug)"
    ),
]

@allure.feature("AR Account Validation")
@allure.story("Validate account with AR payloads")
@pytest.mark.parametrize("payload, expected_status, expected_fields", test_cases)
def test_argentina_accounts(payload, expected_status, expected_fields):
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

    # Validación de los campos, sino se rompe
    for field, expected_value in expected_fields.items():
        keys = field.split(".")
        value = response_json
        for k in keys:
            value = value.get(k, {})
        assert value == expected_value
