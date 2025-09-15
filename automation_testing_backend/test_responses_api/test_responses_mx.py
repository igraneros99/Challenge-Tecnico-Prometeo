import requests
import json

url = "https://account-validation.sandbox.prometeoapi.com/validate-account/"
headers = {
    "accept": "application/json",
    "content-type": "application/x-www-form-urlencoded",
    "X-API-Key": "Ysh7cIDDglVga6AFrKWVXyyXeihmBILDR1ZDCEVCtnaKGE8jghfcoSMAN5gAZMdB"
}

test_cases = [
    {
        "title": "MX valid account - known beneficiary",
        "payload": {
            "account_number": "999000000000000001",
            "country_code": "MX"
        }
    },
    {
        "title": "MX invalid account - not found in sandbox",
        "payload": {
            "account_number": "999000000000000014",
            "country_code": "MX"
        }
    },
    {
        "title": "MX invalid account - too short",
        "payload": {
            "account_number": "123456",
            "country_code": "MX"
        }
    },
    {
        "title": "MX invalid account - contains letters",
        "payload": {
            "account_number": "99900abc00000001",
            "country_code": "MX"
        }
    },
    {
        "title": "MX invalid request - missing account number",
        "payload": {
            "country_code": "MX"
        }
    },
    {
        "title": "MX invalid request - missing country code",
        "payload": {
            "account_number": "999000000000000001"
        }
    },
    {
        "title": "MX valid sandbox account",
        "payload": {
            "account_number": "0",
            "branch_code": "000",
            "bank_code": "999",
            "country_code": "MX"
        }
    },
    {
        "title": "MX invalid sandbox account",
        "payload": {
            "account_number": "1",
            "branch_code": "000",
            "bank_code": "999",
            "country_code": "MX"
        }
    },
    {
        "title": "MX request - missing account number (sandbox-local)",
        "payload": {
            "branch_code": "000",
            "bank_code": "999",
            "country_code": "MX"
        }
    },
    {
        "title": "MX request - branch code contains letters",
        "payload": {
            "account_number": "0",
            "branch_code": "abc",
            "bank_code": "999",
            "country_code": "MX"
        }
    },
    {
        "title": "MX request - bank code with special characters",
        "payload": {
            "account_number": "0",
            "branch_code": "000",
            "bank_code": "99@",
            "country_code": "MX"
        }
    },
    {
        "title": "MX request - invalid country code",
        "payload": {
            "account_number": "0",
            "branch_code": "000",
            "bank_code": "999",
            "country_code": "ZZ"
        }
    }
]

for case in test_cases:
    print(f"\nTest: {case['title']}")
    try:
        response = requests.post(url, headers=headers, data=case["payload"])
        print(f"Status: {response.status_code}")
        try:
            print(json.dumps(response.json(), indent=2, ensure_ascii=False))
        except Exception as e:
            print("JSON parsing error:", e)
            print(response.text)
    except requests.exceptions.RequestException as e:
        print("Connection error:", e)
