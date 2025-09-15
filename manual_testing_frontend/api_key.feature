Feature: API Key Display

  As a logged-in user
  I want to see my API Key clearly in the dashboard
  So I can use it for integrating with Prometeo sandbox

  @happy @en
  Scenario: API Key is displayed after login
    Given I am logged in
    When I navigate to the dashboard
    Then I should see my API Key visible in a code block

  @happy @en
  Scenario: API Key block includes benefits
    Given I am on the dashboard
    Then I should see the API Key section list the following:
      | Fictitious data       |
      | Free and enabled forever |
      | Dashboard available   |
      | Unlimited API calls   |

  @happy @en
  Scenario: API Key does not change across sessions
    Given I log in with valid credentials
    And I navigate to the dashboard
    When I log out and log back in
    Then I should see the same API Key as before

  @unhappy @en
  Scenario: API Key should not be editable
    Given I am on the dashboard
    When I attempt to click or edit the API Key
    Then the input should be read-only

  @unhappy @en
  Scenario: Dashboard fails to display API Key (fallback scenario)
    Given I am logged in
    And the API Key cannot be retrieved from the backend
    Then I should see a warning message or empty state
