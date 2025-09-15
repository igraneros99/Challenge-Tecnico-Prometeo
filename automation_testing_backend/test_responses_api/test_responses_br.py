import requests
import json

URL = "https://account-validation.sandbox.prometeoapi.com/validate-account/"
API_KEY = "Ysh7cIDDglVga6AFrKWVXyyXeihmBILDR1ZDCEVCtnaKGE8jghfcoSMAN5gAZMdB"

headers = {
    "accept": "application/json",
    "content-type": "application/x-www-form-urlencoded",
    "X-API-Key": API_KEY
}

test_cases = [
    {
        "name": "BR valid IBAN",
        "payload": {
            "account_number": "BR7299999999010100000001001C1",
            "country_code": "BR",
            "document_number": "58.547.642/0001-95"
        }
    },
    {
        "name": "BR invalid IBAN",
        "payload": {
            "account_number": "BR3899999999010100000001002C1",
            "country_code": "BR",
            "document_number": "58.547.642/0001-95"
        }
    },
    {
        "name": "BR invalid characters",
        "payload": {
            "account_number": "ABC12345",
            "country_code": "BR",
            "document_number": "58.547.642/0001-95"
        }
    },
    {
        "name": "BR missing account_number",
        "payload": {
            "account_number": "",
            "country_code": "BR",
            "document_number": "58.547.642/0001-95"
        }
    },
    {
        "name": "BR missing country_code",
        "payload": {
            "account_number": "BR7299999999010100000001001C1",
            "document_number": "58.547.642/0001-95"
        }
    },
    {
        "name": "BR invalid alias",
        "payload": {
            "account_number": "prometeo.pruebas.mp",
            "country_code": "BR"
        }
    },
    {
        "name": "BR test IBAN valid",
        "payload": {
            "account_number": "BR3899999999010100000001002C1",
            "country_code": "BR",
            "document_number": "58.547.642/0001-95"
        }
    },
    {
        "name": "BR incorrect account",
        "payload": {
            "account_number": "1002",
            "branch_code": "00001",
            "bank_code": "999",
            "country_code": "BR",
            "document_number": "58.547.642/0001-95",
            "account_type": "CHECKING"
        }
    },
    {
        "name": "BR valid local account",
        "payload": {
            "account_number": "1001",
            "country_code": "BR",
            "document_number": "58.547.642/0001-95",
            "branch_code": "00001",
            "bank_code": "999",
            "account_type": "CHECKING"
        }
    },
    {
        "name": "BR invalid local account",
        "payload": {
            "account_number": "1002",
            "country_code": "BR",
            "document_number": "58.547.642/0001-95",
            "branch_code": "00001",
            "bank_code": "999",
            "account_type": "CHECKING"
        }
    },
    {
        "name": "BR alphanumeric account_number",
        "payload": {
            "account_number": "ABCD1234",
            "country_code": "BR",
            "document_number": "58.547.642/0001-95",
            "branch_code": "00001",
            "bank_code": "999",
            "account_type": "CHECKING"
        }
    },
    {
        "name": "BR malformed document_number",
        "payload": {
            "account_number": "1001",
            "country_code": "BR",
            "document_number": "58547642000195",
            "branch_code": "00001",
            "bank_code": "999",
            "account_type": "CHECKING"
        }
    },
    {
        "name": "BR long branch_code",
        "payload": {
            "account_number": "1001",
            "country_code": "BR",
            "document_number": "58.547.642/0001-95",
            "branch_code": "000011234",
            "bank_code": "999",
            "account_type": "CHECKING"
        }
    },
    {
        "name": "BR unsupported account_type",
        "payload": {
            "account_number": "1001",
            "country_code": "BR",
            "document_number": "58.547.642/0001-95",
            "branch_code": "00001",
            "bank_code": "999",
            "account_type": "INVESTMENT"
        }
    },
    {
        "name": "BR invalid country_code",
        "payload": {
            "account_number": "1001",
            "country_code": "ZZ",
            "document_number": "58.547.642/0001-95",
            "branch_code": "00001",
            "bank_code": "999",
            "account_type": "CHECKING"
        }
    }
]

for case in test_cases:
    print(f"\nTest: {case['name']}")
    try:
        response = requests.post(URL, headers=headers, data=case["payload"], timeout=10)
        print(f"Status: {response.status_code}")
        try:
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        except Exception as e:
            print("JSON parsing error:", e)
            print(response.text)
    except requests.exceptions.RequestException as e:
        print("Connection error:", e)
