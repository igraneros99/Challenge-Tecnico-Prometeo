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
        {"account_number": "999000000000000001", "country_code": "MX"},
        200,
        {
            "data.valid": True,
            "data.message": "Cuenta valida",
            "data.beneficiary_name": "BANCO DE TAPITAS AC",
            "data.country_code": "MX",
            "data.document_type": "RFC",
            "data.document_number": "BTA160616Q24"
        },
        id="MX_Valid_KnownBeneficiary"
    ),
    pytest.param(
        {"account_number": "999000000000000014", "country_code": "MX"},
        404,
        {
            "data.valid": False,
            "errors.code": 404,
            "errors.message": "Cuenta credito invalida"
        },
        id="MX_Invalid_AccountNotFound"
    ),
    pytest.param(
        {"account_number": "123456", "country_code": "MX"},
        400,
        {
            "errors.code": 400,
            "errors.message": "Missing parameter: branch_code"
        },
        id="MX_Invalid_AccountTooShort"
    ),
    pytest.param(
        {"account_number": "99900abc00000001", "country_code": "MX"},
        400,
        {
            "errors.code": 400,
            "errors.message": "Missing parameter: bank_code"
        },
        id="MX_Invalid_AccountWithLetters"
    ),
    pytest.param(
        {"country_code": "MX"},
        400,
        {
            "errors.code": 400,
            "errors.message": "Missing parameter: account_number"
        },
        id="MX_Invalid_MissingAccountNumber"
    ),
    pytest.param(
        {"account_number": "999000000000000001"},
        400,
        {
            "errors.code": 400,
            "errors.message": "Missing parameter: country_code"
        },
        id="MX_Invalid_MissingCountryCode"
    ),
    pytest.param(
        {"account_number": "0", "branch_code": "000", "bank_code": "999", "country_code": "MX"},
        200,
        {
            "data.valid": True,
            "data.message": "Cuenta valida",
            "data.beneficiary_name": "BANCO DE TAPITAS AC",
            "data.document_type": "RFC",
            "data.document_number": "BTA160616Q24"
        },
        id="MX_Valid_SandboxDefaultAccount"
    ),
    pytest.param(
        {"account_number": "1", "branch_code": "000", "bank_code": "999", "country_code": "MX"},
        404,
        {
            "data.valid": False,
            "errors.code": 404,
            "errors.message": "Cuenta credito invalida"
        },
        id="MX_Invalid_SandboxDefaultWrongAccount"
    ),
    pytest.param(
        {"branch_code": "000", "bank_code": "999", "country_code": "MX"},
        400,
        {
            "errors.code": 400,
            "errors.message": "Missing parameter: account_number"
        },
        id="MX_Invalid_SandboxMissingAccountNumber"
    ),
    pytest.param(
        {"account_number": "0", "branch_code": "abc", "bank_code": "999", "country_code": "MX"},
        500,
        {
            "errors.code": 500,
            "errors.message": "Error interno"
        },
        id="MX_Invalid_BranchCodeLetters"
    ),
    pytest.param(
        {"account_number": "0", "branch_code": "000", "bank_code": "99@", "country_code": "MX"},
        400,
        {
            "errors.code": 400,
            "errors.message": "Invalid parameter: bank_code"
        },
        id="MX_Invalid_BankCodeSymbols"
    ),
    pytest.param(
        {"account_number": "0", "branch_code": "000", "bank_code": "999", "country_code": "ZZ"},
        400,
        {
            "errors.code": 400,
            "errors.message": "Invalid parameter: country_code"
        },
        id="MX_Invalid_CountryCodeZZ"
    )
]

@allure.feature("MX Account Validation")
@allure.story("Validate account with MX payloads")
@pytest.mark.parametrize("payload, expected_status, expected_fields", test_cases)
def test_mexico_accounts(payload, expected_status, expected_fields):
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
