import pytest
import requests
import allure
import json

URL = "https://account-validation.sandbox.prometeoapi.com/validate-account/"
API_KEY = "Ysh7cIDDglVga6AFrKWVXyyXeihmBILDR1ZDCEVCtnaKGE8jghfcoSMAN5gAZMdB"

HEADERS = {
    "accept": "application/json",
    "content-type": "application/x-www-form-urlencoded",
    "X-API-Key": API_KEY,
}

test_cases = [
    pytest.param(
        {"account_number": "BR7299999999010100000001001C1", "country_code": "BR", "document_number": "58.547.642/0001-95"},
        200,
        {"data.valid": True, "data.beneficiary_name": "JOÃO DAS NEVES"},
        id="BR valid IBAN"
    ),
    pytest.param(
        {"account_number": "BR3899999999010100000001002C1", "country_code": "BR", "document_number": "58.547.642/0001-95"},
        404,
        {"data.valid": False, "errors.message": "Cuenta credito invalida"},
        id="Br invalid IBAN"
    ),
        # IMPORTANTE ! Este test se ejecuta pero no se refleja en allure por bug conocido del reporter
    pytest.param(
        {"account_number": "ABC12345", "country_code": "BR", "document_number": "58.547.642/0001-95"},
        400,
        {"errors.message": "Missing parameter: bk_code"},
        id="BR invalid characters"
    ),
    pytest.param(
        {"account_number": "", "country_code": "BR", "document_number": "58.547.642/0001-95"},
        400,
        {"errors.message": "Missing parameter: bk_code"},
        id="BR missing account_number"
    ),
    pytest.param(
        {"account_number": "BR7299999999010100000001001C1", "document_number": "58.547.642/0001-95"},
        400,
        {"errors.message": "Missing parameter: country_code"},
        id="BR missing country_code"
    ),
    pytest.param(
        {"account_number": "prometeo.pruebas.mp", "country_code": "BR"},
        400,
        {"errors.message": "Missing parameter: bk_code"},
        id="BR invalid alias"
    ),
    pytest.param(
        {"account_number": "BR3899999999010100000001002C1", "country_code": "BR", "document_number": "58.547.642/0001-95"},
        404,
        {"data.valid": False, "errors.message": "Cuenta credito invalida"},
        id="BR test IBAN valid"
    ),
    pytest.param(
        {"account_number": "1002", "branch_code": "00001", "bank_code": "999", "country_code": "BR", "document_number": "58.547.642/0001-95", "account_type": "CHECKING"},
        404,
        {"data.valid": False, "errors.message": "Cuenta credito invalida"},
        id="BR Invalid account"
    ),
    # IMPORTANTE ! Este test se ejecuta pero no se refleja en allure por bug conocido del reporter
    pytest.param(
        {"account_number": "1001", "branch_code": "00001", "bank_code": "999", "country_code": "BR", "document_number": "58.547.642/0001-95", "account_type": "CHECKING"},
        200,
        {"data.valid": True, "data.account_number": "1001", "data.bank_code": "999", "data.country_code": "BR", "data.beneficiary_name": "JOÃO DAS NEVES", "data.account_type": "CHECKING", "data.account_currency": "BRL"},
        id="BR valid local account"
    ),
    pytest.param(
        {"account_number": "1002", "branch_code": "00001", "bank_code": "999", "country_code": "BR", "document_number": "58.547.642/0001-95", "account_type": "CHECKING"},
        404,
        {"data.valid": False, "errors.message": "Cuenta credito invalida"},
        id="BR invalid local account"
    ),
    pytest.param(
        {"account_number": "ABCD1234", "branch_code": "00001", "bank_code": "999", "country_code": "BR", "document_number": "58.547.642/0001-95", "account_type": "CHECKING"},
        404,
        {"data.valid": False, "errors.message": "Cuenta credito invalida"},
        id="BR alphanumeric account_number"
    ),
    pytest.param(
        {"account_number": "1001", "branch_code": "00001", "bank_code": "999", "country_code": "BR", "document_number": "58547642000195", "account_type": "CHECKING"},
        200,
        {"data.valid": True, "data.message": "Cuenta valida"},
        id="BR malformed document number"
    ),
    pytest.param(
        {"account_number": "1001", "branch_code": "000011234", "bank_code": "999", "country_code": "BR", "document_number": "58.547.642/0001-95", "account_type": "CHECKING"},
        400,
        {"errors.message": "Invalid parameter: branch_code"},
        id="BR long branch_code"
    ),
    pytest.param(
        {"account_number": "1001", "branch_code": "00001", "bank_code": "999", "country_code": "BR", "document_number": "58.547.642/0001-95", "account_type": "INVESTMENT"},
        400,
        {"errors.message": "Invalid parameter: account_type"},
        id="BR unsupported account_type"
    ),
    pytest.param(
        {"account_number": "1001", "branch_code": "00001", "bank_code": "999", "country_code": "ZZ", "document_number": "58.547.642/0001-95", "account_type": "CHECKING"},
        400,
        {"errors.message": "Invalid parameter: country_code"},
        id="BR invalid country_code"
    ),
]

@allure.feature("BR Account Validation")
@allure.story("Validate account with BR payloads")
@pytest.mark.parametrize("payload, expected_status, expected_fields", test_cases)
def test_brazil_accounts(payload, expected_status, expected_fields):
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
