@happy @manual @en
Scenario: Successful registration with valid data and email verification
  Given the user accesses the registration form
  And fills in the following valid fields:
    | Field                | Value                  |
    | First Name           | Ignacio                |
    | Last Name            | Graneros               |
    | Company Name         | Ignacio Company        |
    | Corporate Email      | ignacio@devopsqa.com   |
    | Password             | Devops123!             |
    | Confirm Password     | Devops123!             |
    | Solution             | Borderless Banking     |
  And accepts the terms and conditions
  When clicking the "Register" button
  Then the user should see a message stating that a verification email has been sent
  And the user receives an email with the subject "Verify your account"
  When the user clicks the verification link in the email
  Then the account should be marked as verified in the system
  And the user should be able to log in successfully using the registered credentials

# Nota: La verificacion de email se puede automatizar usando MailSlurp.

@unhappy @manual @en
Scenario: Failed registration due to existing email
  Given a user is already registered with the email ignacio@devopsqa.com
  And the user accesses the registration form
  And fills in the fields as follows:
    | Field                | Value                  |
    | First Name           | Ignacio                |
    | Last Name            | Graneros               |
    | Company Name         | Ignacio Company        |
    | Corporate Email      | ignacio@devopsqa.com   |
    | Password             | Devops123!             |
    | Confirm Password     | Devops123!             |
    | Solution             | CEP                    |
  And accepts the terms and conditions
  When clicking the "Register" button
  Then the user should see an error message indicating that the email is already in use
  And no new account should be created in the database
