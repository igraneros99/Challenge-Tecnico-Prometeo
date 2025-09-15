@account_validation
Feature: Bank Account Validation
  API Endpoint: POST /validate-account/
  Description: Validate account numbers and retrieve banking details for the AR, BR, CO, MX accounts.

  ########################
  # ARGENTINA (AR) CASES #
  ########################

  @ar @happy @api @en
  Scenario: Validate AR account number (valid input)
    Given the API is available
    When I send a POST request to the validation endpoint with:
      | account_number   | 9990000100000000000000 |
      | country_code     | AR                     |
      | document_number  | 30-71515454-1          |
    Then the response code should be 200
    And the response field "data.valid" should be true
    And the response field "data.beneficiary_name" should be "ROBERTO CARLOS"

  @ar @unhappy @api @en @sandbox-bug
  Scenario: Validate AR account with malformed account number
    Given the API is available
    When I send a POST request to the validation endpoint with:
      | account_number   | abcd1234               |
      | country_code     | AR                     |
      | document_number  | 30-71515454-1          |
    Then the request may timeout due to sandbox issue
    And no status code or error message may be returned
  # En sandbox, puede colgarse sin dar respuesta

  @ar @unhappy @api @en @sandbox-bug
  Scenario: Validate AR account with missing account number
    Given the API is available
    When I send a POST request to the validation endpoint with:
      | account_number   |                         |
      | country_code     | AR                      |
      | document_number  | 30-71515454-1           |
    Then the response code should be 400
    And the response field "errors.message" should be "Missing parameter: account_number"
  # El sandbox ahora devuelve 400 correctamente, pero ocasionalmente responde 500. Posible bug intermitente ?

  @ar @unhappy @api @en
  Scenario: Validate AR account with missing country code
    Given the API is available
    When I send a POST request to the validation endpoint with:
      | account_number   | 0720000300000001354934 |
      | document_number  | 30-71515454-1          |
    Then the response code should be 400
    And the response field "errors.code" should be 400
    And the response field "errors.message" should be "Missing parameter: country_code"
  # Este caso sí devuelve un 400 correctamente con el country_code invalido.

@ar @unhappy @api @en @sandbox-bug
Scenario: Invalid account sandobox but returns valid = true
    Given the API is available
    When I send a POST request to the validation endpoint with:
      | account_number   | 9990000000000000000017 |
      | country_code     | AR                     |
      | document_number  | 30-71515454-1          |
   Then the response code should be 200
    And the response field "data.valid" should be true
    And the response field "data.beneficiary_name" should be "ROBERTO CARLOS"
  # En sandbox, devuelve valid=true aunque la cuenta sea ficticia. No se va a automatizar por que es un caso con bug y flaky por naturaleza.

  @ar @happy @api @en
  Scenario: Validate AR alias account (valid)
    Given the API is available
    When I send a POST request to the validation endpoint with:
      | account_number   | prometeo.pruebas.mp     |
      | country_code     | AR                      |
  Then the response code should be 200
  And the response field "data.valid" should be true
  And the response field "data.beneficiary_name" should be "ROBERTO CARLOS"
  And the response field "data.account_type" should be "CHECKING"
  And the response field "data.account_currency" should be "ARS"
  # Caso positivo usando un alias como número de cuenta.

  @ar @unhappy @api @en @sandbox-bug
  Scenario: Validate AR alias account (invalid alias)
    Given the API is available
    When I send a POST request to the validation endpoint with:
      | account_number   | prometeofallo.pruebas.mp |
      |  country_code     | AR                       |
    Then the response code should be 500
    And the response field "errors.code" should be 500
    And the response field "errors.message" should be "Error interno"
  # Debería devolver 404 o 422, pero devuelve 500 o timeout. Bug en el sandbox.

  ########################
  # BRAZIL (BR) CASES    #
  ########################

  @br @happy @api @en
  Scenario: Validate BR account with IBAN (valid)
    Given the API is available
    When I send a POST request to the validation endpoint with:
      | account_number   | BR7299999999010100000001001C1 |
      | country_code     | BR                            |
      | document_number  | 58.547.642/0001-95            |
    Then the response code should be 200
    And the response field "data.valid" should be true
    And the response field "data.beneficiary_name" should exist

  @br @unhappy @api @en
  Scenario: Validate BR account with IBAN (invalid)
    Given the API is available
    When I send a POST request to the validation endpoint with:
      | account_number   | BR3899999999010100000001002C1 |
      | country_code     | BR                            |
      | document_number  | 58.547.642/0001-95            |
    Then the response code should be 404
    And the response field "data.valid" should be false
    And the response field "errors.message" should be "Cuenta credito invalida"

  @br @unhappy @api @en @sandbox-bug
  Scenario: Validate BR account with invalid characters (sandbox may respond inconsistently)
    Given the API is available
    When I send a POST request to the validation endpoint with:
      | account_number   | ABC12345                      |
      | country_code     | BR                            |
      | document_number  | 58.547.642/0001-95            |
    Then the response code should be 400
    And the response field "errors.message" should be "Missing parameter: bk_code"
  # Limitacion del sandbox cuando se usa el IBAN directamente

  @br @unhappy @api @en @sandbox-bug
  Scenario: Validate BR account with missing account number
    Given the API is available
    When I send a POST request to the validation endpoint with:
      | account_number   |                               |
      | country_code     | BR                            |
      | document_number  | 58.547.642/0001-95            |
    Then the response code should be 400
    And the response field "errors.message" should be "Missing parameter: bk_code"
  # Limitacion del sandbox cuando se usa el IBAN directamente

  @br @unhappy @api @en
  Scenario: Validate BR account with missing country code
    Given the API is available
    When I send a POST request to the validation endpoint with:
      | account_number   | BR7299999999010100000001001C1 |
      | document_number  | 58.547.642/0001-95            |
    Then the response code should be 400
    And the response field "errors.code" should be 400
    And the response field "errors.message" should be "Missing parameter: country_code"

  @br @unhappy @api @en @sandbox-bug
  Scenario: Validate BR account with alias (invalid, should reject)
    Given the API is available
    When I send a POST request to the validation endpoint with:
      | account_number   | prometeo.pruebas.mp           |      # account_number sacado de los casos de AR
      | country_code     | BR                            |
    Then the response code should be 400
    And the response field "errors.message" should be "Missing parameter: bk_code"
  # En BR, los alias no deberían usarse. El sandbox no reconoce alias y responde con error de parámetro faltante.

  @br @happy @api @en @sandbox-bug
  Scenario: Validate BR account using test IBAN (valid)
    Given the API is available
    When I send a POST request to the validation endpoint with:
      | account_number    | BR3899999999010100000001002C1 |
      | country_code      | BR                            |
      | document_number   | 58.547.642/0001-95            |
    Then the response code should be 200
    And the response field "data.valid" should be true
    And the response field "data.beneficiary_name" should be "JOÃO DAS NEVES"
    And the response field "data.account_type" should be "CHECKING"
    And the response field "data.account_currency" should be "BRL"

  @br @unhappy @api @en @sandbox-bug
  Scenario: Validate BR account with incorrect account data (should fail)
    Given the API is available
    When I send a POST request to the validation endpoint with:
      | account_number    | 1002                         |
      | branch_code       | 00001                        |
      | bank_code         | 999                          |
      | country_code      | BR                           |
      | document_number   | 58.547.642/0001-95           |
      | account_type      | CHECKING                     |
    Then the response code should be 404
    And the response field "data.valid" should be false
    And the response field "errors.code" should be 404
    And the response field "errors.message" should be "Cuenta credito invalida"
  # Parámetros individuales incorrectos. El sandbox responde con 404 y mensaje de error.

  @br @happy @api @en
  Scenario: Valid BR account - sandbox-local
    Given the account validation API is available
    When I send a POST request with:
      | account_number   | 1001                          |
      | country_code     | BR                            |
      | document_number  | 58.547.642/0001-95            |
      | branch_code      | 00001                         |
      | bank_code        | 999                           |
      | account_type     | CHECKING                      |
    Then the response status should be 200
    And the response field "data.valid" should be true
    And the response field "data.account_number" should be "1001"
    And the response field "data.bank_code" should be "999"
    And the response field "data.country_code" should be "BR"
    And the response field "data.beneficiary_name" should be "JOÃO DAS NEVES"
    And the response field "data.account_type" should be "CHECKING"
    And the response field "data.account_currency" should be "BRL"

  @br @unhappy @api @en
  Scenario: Invalid BR account - sandbox-local
    Given the account validation API is available
    When I send a POST request with:
      | account_number   | 1002                          |
      | country_code     | BR                            |
      | document_number  | 58.547.642/0001-95            |
      | branch_code      | 00001                         |
      | bank_code        | 999                           |
      | account_type     | CHECKING                      |
    Then the response status should be 404
    And the response field "data.valid" should be false
    And the response field "errors.code" should be 404
    And the response field "errors.message" should be "Cuenta credito invalida"

  @br @unhappy @api @en
  Scenario: Invalid BR account - alphanumeric account number
    Given the account validation API is available
    When I send a POST request with:
      | account_number   | ABCD1234                   |
      | country_code     | BR                         |
      | document_number  | 58.547.642/0001-95         |
      | branch_code      | 00001                      |
      | bank_code        | 999                        |
      | account_type     | CHECKING                   |
    Then the response status should be 404
    And the response field "errors.code" should be 404
    And the response field "errors.message" should be "Cuenta credito invalida"

  @br @unhappy @api @en @sandbox-bug
  Scenario: Invalid BR account - malformed document number
    Given the account validation API is available
    When I send a POST request with:
      | account_number   | 1001                    |
      | country_code     | BR                      |
      | document_number  | 58547642000195          |
      | branch_code      | 00001                   |
      | bank_code        | 999                     |
      | account_type     | CHECKING                |
    Then the response status should be 200
    And the response field "data.valid" should be true
    And the response field "data.message" should be "Cuenta valida"
  # No entiendo por que pero el documento esta malformado y aun asi responde bien el api (faltan puntos, slashes, etc),
  # El api devuelve 200 y lo considero valido.
  # Normalizacion interna o validacion faltante seguramente.

  @br @unhappy @api @en
  Scenario: Invalid BR account - branch code too long
    Given the account validation API is available
   When I send a POST request with:
      | account_number   | 1001                          |
      | country_code     | BR                            |
      | document_number  | 58.547.642/0001-95            |
      | branch_code      | 000011234                     |
      | bank_code        | 999                           |
      | account_type     | CHECKING                      |
    Then the response status should be 400
    And the response field "errors.code" should be 400
    And the response field "errors.message" should be "Invalid parameter: branch_code"

  @br @unhappy @api @en
  Scenario: Invalid BR account - unsupported account type
    Given the account validation API is available
    When I send a POST request with:
      | account_number   | 1001                          |
      | country_code     | BR                            |
      | document_number  | 58.547.642/0001-95            |
      | branch_code      | 00001                         |
      | bank_code        | 999                           |
      | account_type     | INVESTMENT                    |
    Then the response status should be 400
    And the response field "errors.code" should be 400
    And the response field "errors.message" should be "Invalid parameter: account_type"

  @br @unhappy @api @en
  Scenario: Invalid BR account - unknown country code
    Given the account validation API is available
    When I send a POST request with:
      | account_number   | 1001                          |
      | country_code     | ZZ                            |
      | document_number  | 58.547.642/0001-95            |
      | branch_code      | 00001                         |
      | bank_code        | 999                           |
      | account_type     | CHECKING                      |
    Then the response status should be 400
    And the response field "errors.code" should be 400
    And the response field "errors.message" should be "Invalid parameter: country_code"

  ########################
  # COLOMBIA (CO) CASES  #
  ########################

  @co @happy @api @en
  Scenario: Valid CO account should respond with status or fail gracefully
    Given a valid account number "000000001", bank code "1007" and country code "CO"
    When I submit the validation request
    Then the status code should be 200 or 500 or timeout
    And the response should contain valid = true if sandbox is up
  # Timeout o error 500. El sandbox de CO no responde consistentemente ni en requests manuales ni automáticos.

  @co @unhappy @api @en
  Scenario: Invalid CO account returns server error or no response
    Given an invalid account number "999999999", bank code "1007" and country code "CO"
    When I submit the validation request
    Then the response should return 500 or timeout
    And the field "valid" may not be returned
  # Timeout o error 500. El sandbox de CO no responde consistentemente ni en requests manuales ni automáticos.

  ########################
  # MEXICO (MX) CASES    #
  ########################

  @mx @happy @api @en
  Scenario: Valid MX account - known beneficiary
    Given the account validation API is available
    When I send a POST request with:
      | account_number | 999000000000000001 |
      | country_code   | MX                 |
    Then the response status should be 200
    And the response field "data.valid" should be true
    And the response field "data.message" should be "Cuenta valida"
    And the response field "data.beneficiary_name" should be "BANCO DE TAPITAS AC"
    And the response field "data.country_code" should be "MX"
    And the response field "data.document_type" should be "RFC"
    And the response field "data.document_number" should be "BTA160616Q24"

  @mx @unhappy @api @en
  Scenario: Invalid MX account - account not found in sandbox
    Given the account validation API is available
    When I send a POST request with:
      | account_number | 999000000000000014 |
      | country_code   | MX                 |
    Then the response status should be 404
    And the response field "data.valid" should be false
    And the response field "errors.code" should be 404
    And the response field "errors.message" should be "Cuenta credito invalida"

  @mx @unhappy @api @en @sandox-bug
  Scenario: Invalid MX account - account number too short
    Given the account validation API is available
    When I send a POST request with:
      | account_number | 123456  |
      | country_code   | MX      |
    Then the response status should be 404
    And the response field "errors.code" should be 404
    And the response field "errors.message" should be "Missing parameter: branch_code"
  # el mensaje de error refiere al branch code cuando el account number es demasiado corto

  @mx @unhappy @api @en @sandbox-bug
  Scenario: Invalid MX account - account number contains letters
    Given the account validation API is available
    When I send a POST request with:
      | account_number | 99900abc00000001  |
      | country_code   | MX                |
    Then the response status should be 400
    And the response field "errors.code" should be 400
    And the response field "errors.message" should be "Missing parameter: bank_code"
  # El parametro de bankcode no esta siendo resuelto por poner numeros en el account ?

  @mx @unhappy @api @en
  Scenario: Invalid MX account - missing account number
    Given the account validation API is available
    When I send a POST request with:
      | country_code   | MX                |
    Then the response status should be 400
    And the response field "errors.code" should be 400
    And the response field "errors.message" should be "Missing parameter: account_number"

  @mx @unhappy @api @en
  Scenario: Invalid MX account - missing country code
    Given the account validation API is available
    When I send a POST request with:
      | account_number | 999000000000000001 |
    Then the response status should be 400
    And the response field "errors.code" should be 400
    And the response field "errors.message" should be "Missing parameter: country_code"

  @mx @happy @api @en
  Scenario: Valid MX sandbox account
    Given the account validation API is available
    When I send a POST request with:
      | account_number | 0   |
      | branch_code    | 000 |
      | bank_code      | 999 |
      | country_code   | MX  |
    Then the response status should be 200
    And the response field "data.valid" should be true
    And the response field "data.message" should be "Cuenta valida"
    And the response field "data.beneficiary_name" should be "BANCO DE TAPITAS AC"
    And the response field "data.document_type" should be "RFC"
    And the response field "data.document_number" should be "BTA160616Q24"

    @mx @unhappy @api @en
    Scenario: Invalid MX sandbox account
    Given the account validation API is available
    When I send a POST request with:
      | account_number | 1   |
      | branch_code    | 000 |
      | bank_code      | 999 |
      | country_code   | MX  |
    Then the response status should be 404
    And the response field "data.valid" should be false
    And the response field "errors.code" should be 404
    And the response field "errors.message" should be "Cuenta credito invalida"

  @mx @unhappy @sandbox-local @api @en
  Scenario: Invalid MX request - missing account number
    Given the account validation API is available
    When I send a POST request with:
      | branch_code    | 000 |
      | bank_code      | 999 |
      | country_code   | MX  |
    Then the response status should be 400
    And the response field "errors.code" should be 400
    And the response field "errors.message" should be "Missing parameter: account_number"

  @mx @unhappy @sandbox-local @api @en
  Scenario: Invalid MX request - branch code contains letters
    Given the account validation API is available
    When I send a POST request with:
      | account_number | 0     |
      | branch_code    | abc   |
      | bank_code      | 999   |
      | country_code   | MX    |
    Then the response status should be 400
    And the response field "errors.code" should be 400
    And the response field "errors.message" should be "Invalid parameter: branch_code"
  # Bug muy grave, deberia de retornar un 400 con el mensaje de invalid parameter account_number, pero no un error interno del servidor, todo apunta a que falta una validacion al formato de branch_code, al procesar un string como si fuera un numero se rompe el backend ( Conversion fallida o acceso invalido ?)


  @mx @unhappy @sandbox-local @api @en
  Scenario: Invalid MX request - bank code with special characters
    Given the account validation API is available
    When I send a POST request with:
      | account_number | 0     |
      | branch_code    | 000   |
      | bank_code      | 99@   |
      | country_code   | MX    |
    Then the response status should be 400
    And the response field "errors.code" should be 400
    And the response field "errors.message" should be "Invalid parameter: bank_code"

    @mx @unhappy @sandbox-local @api @en
  Scenario: Invalid MX request - invalid country code
    Given the account validation API is available
    When I send a POST request with:
      | account_number | 0     |
      | branch_code    | 000   |
      | bank_code      | 999   |
      | country_code   | ZZ    |
    Then the response status should be 400
    And the response field "errors.code" should be 400
    And the response field "errors.message" should be "Invalid parameter: country_code"
