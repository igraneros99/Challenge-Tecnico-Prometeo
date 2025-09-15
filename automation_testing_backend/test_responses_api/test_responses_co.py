import requests
import time

url = "https://account-validation.sandbox.prometeoapi.com/validate-account/"
headers = {
    "accept": "application/json",
    "content-type": "application/x-www-form-urlencoded",
    "X-API-Key": "Ysh7cIDDglVga6AFrKWVXyyXeihmBILDR1ZDCEVCtnaKGE8jghfcoSMAN5gAZMdB"
}

# valido, manejo de parametros
payload_valid = {
    "account_number": "000000001",
    "country_code": "CO",
    "document_number": "123456789",
    "document_type": "CC",
    "bank_code": "1007",
    "account_type": "CHECKING"
}

# si no funciona en 10 segundos timeout
print("=== CO valid ===")
start = time.time()
try:
    response = requests.post(url, data=payload_valid, headers=headers, timeout=10)
    duration = time.time() - start
    print(f"Status code: {response.status_code}")
    print(f"Response time: {duration:.2f} sec")
    print(response.text)
except requests.exceptions.Timeout:
    print("Timeout after 10 seconds.")
except requests.exceptions.RequestException as e:
    print(f"Connection error: {e}")

# invalido, manejo de los parametros
payload_invalid = {
    "account_number": "999999999",
    "country_code": "CO",
    "document_number": "123456789",
    "document_type": "CC",
    "bank_code": "1007",
    "account_type": "CHECKING"
}

# si no funciona en 10 segundos timeout
print("\n=== CO invalid ===")
start = time.time()
try:
    response = requests.post(url, data=payload_invalid, headers=headers, timeout=10)
    duration = time.time() - start
    print(f"Status code: {response.status_code}")
    print(f"Response time: {duration:.2f} sec")
    print(response.text)
except requests.exceptions.Timeout:
    print("Timeout after 10 seconds.")
except requests.exceptions.RequestException as e:
    print(f"Connection error: {e}")

#se puede implementar un helper para el timeout y llamarlo directamente, pero para manejo preciso es suficiente hacerlo con esta implementacion