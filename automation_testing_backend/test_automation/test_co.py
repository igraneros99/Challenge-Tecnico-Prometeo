import pytest
import requests
import allure

BASE_URL = "https://account-validation.sandbox.prometeoapi.com/validate-account/"
HEADERS = {
    "accept": "application/json",
    "content-type": "application/x-www-form-urlencoded",
    "X-API-Key": "Ysh7cIDDglVga6AFrKWVXyyXeihmBILDR1ZDCEVCtnaKGE8jghfcoSMAN5gAZMdB"
}

test_cases = [
    pytest.param(
        {"account_number": "000000001", "country_code": "CO", "document_number": "123456789", "document_type": "CC", "bank_code": "1007", "account_type": "CHECKING"},
        200,
        {},
        id="CO valid account"
    ),
    pytest.param(
        {"account_number": "999999999", "country_code": "CO", "document_number": "123456789", "document_type": "CC", "bank_code": "1007", "account_type": "CHECKING"},
        422,
        {},
        id="CO invalid account"
    )
]

@allure.feature("CO Account Validation")
@allure.story("Validate account with CO payloads")
@pytest.mark.parametrize("payload, expected_status, expected_response_body", test_cases)
def test_co_account_validation(payload, expected_status, expected_response_body):
    with allure.step("Enviar solicitud POST con payload y headers definidos"):
        try:
            response = requests.post(BASE_URL, data=payload, headers=HEADERS, timeout=10)
        except requests.exceptions.Timeout:
            pytest.fail("Request timed out after 10 seconds")
        except requests.exceptions.RequestException as e:
            pytest.fail(f"Request failed: {e}")

    with allure.step(f"Verificar código de estado esperado: {expected_status}"):
        assert response.status_code == expected_status, f"Expected {expected_status}, got {response.status_code}"

    with allure.step("Adjuntar respuesta al reporte Allure"):
        allure.attach(
            response.text,
            name="Response Body",
            attachment_type=allure.attachment_type.JSON
        )
