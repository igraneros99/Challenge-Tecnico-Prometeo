Feature: User Login

  As a registered user
  I want to log in to the Prometeo dashboard
  So I can access my API key and other features

  @happy @en
  Scenario: Successful login with valid credentials
    Given I navigate to the login page
    When I enter a valid email and valid password
    And I click the login button
    Then I should be redirected to the dashboard URL

  @happy @en
  Scenario: Email input accepts valid format
    Given I navigate to the login page
    When I enter a properly formatted email
    Then the email field should accept the input

  @happy @en
  Scenario: Password field masks characters
    Given I navigate to the login page
    When I type a password into the field
    Then the characters should appear as dots or asterisks

  @happy @en
  Scenario: User can log in again after logout
    Given I am logged in
    And I click the logout button
    When I log in again with valid credentials
    Then I should be redirected to the dashboard URL

  @happy @en
  Scenario: Login fails with incorrect password (expected negative validation)
    Given I navigate to the login page
    When I enter a valid email and an incorrect password
    And I click the login button
    Then I should see the error message "Your account is invalid"

  @unhappy @en
  Scenario: Login with unregistered email
    Given I navigate to the login page
    When I enter an unregistered email and any password
    And I click the login button
    Then I should see the error message "Your account is invalid"

  @unhappy @en
  Scenario: Login with invalid email format
    Given I navigate to the login page
    When I enter an invalid email format
    And I click the login button
    Then I should see the error message "Your account is invalid"

  @unhappy @en
  Scenario: Login with empty fields
    Given I navigate to the login page
    When I leave email and password fields empty
    And I click the login button
    Then I should see the error message "Your account is invalid"

  @unhappy @en
  Scenario: Login with leading/trailing spaces in email
    Given I navigate to the login page
    When I enter valid credentials with spaces around the email
    And I click the login button
    Then I should see the error message "Your account is invalid"

  @unhappy @en
  Scenario: Login with password shorter than expected
    Given I navigate to the login page
    When I enter a valid email and a 2-character password
    And I click the login button
    Then I should see the error message "Your account is invalid"
