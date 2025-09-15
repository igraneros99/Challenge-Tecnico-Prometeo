import requests

url = "https://account-validation.sandbox.prometeoapi.com/validate-account/"
headers = {
    "accept": "application/json",
    "content-type": "application/x-www-form-urlencoded",
    "X-API-Key": "Ysh7cIDDglVga6AFrKWVXyyXeihmBILDR1ZDCEVCtnaKGE8jghfcoSMAN5gAZMdB"
}

test_cases = [
    {
        "name": "Valid AR account number",
        "data": {
            "account_number": "9990000100000000000000",
            "country_code": "AR",
            "document_number": "30-71515454-1"
        }
    },
    {
        "name": "Malformed account number",
        "data": {
            "account_number": "abcd1234",
            "country_code": "AR",
            "document_number": "30-71515454-1"
        }
    },
    {
        "name": "Missing account number",
        "data": {
            "account_number": "",
            "country_code": "AR",
            "document_number": "30-71515454-1"
        }
    },
    {
        "name": "Missing country code",
        "data": {
            "account_number": "0720000300000001354934",
            "document_number": "30-71515454-1"
        }
    },
    {
        "name": "Invalid but returns valid=true (sandbox bug)",
        "data": {
            "account_number": "9990000000000000000017",
            "country_code": "AR",
            "document_number": "30-71515454-1"
        }
    },
    {
        "name": "Valid alias account",
        "data": {
            "account_number": "prometeo.pruebas.mp",
            "country_code": "AR"
        }
    },
    {
        "name": "Invalid alias account (sandbox bug)",
        "data": {
            "account_number": "prometeofallo.pruebas.mp",
            "country_code": "AR"
        }
    }
]

for i, test in enumerate(test_cases, 1):
    print(f"\n--- Test {i}: {test['name']} ---")
    try:
        response = requests.post(url, data=test["data"], headers=headers, timeout=10)
        print(f"Status Code: {response.status_code}")
        try:
            json_resp = response.json()
            print("Response JSON:", json_resp)
        except:
            print("No JSON response.")
    except Exception as e:
        print("Error:", e)
