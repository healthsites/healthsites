Feature: URL availability
  Healthsites exposes many Django URL patterns. This feature guards against
  accidental regressions by confirming that every URL that does not require
  path parameters can still be requested successfully.

  Background:
    Given the list of non-parameterized URLs is prepared

  Scenario: / responds successfully
    When I request "/"
    Then the response should return a successful status code

  Scenario: /about responds successfully
    When I request "/about"
    Then the response should return a successful status code

  Scenario: /admin/core/sitepreferences/ responds successfully
    When I request "/admin/core/sitepreferences/"
    Then the response should return a successful status code

  Scenario: /api/docs/ responds successfully
    When I request "/api/docs/"
    Then the response should return a successful status code

  Scenario: /api/public/countries/autocomplete responds successfully
    When I request "/api/public/countries/autocomplete"
    Then the response should return a successful status code

  Scenario: /api/public/csv-import-progress/ responds successfully
    When I request "/api/public/csv-import-progress/"
    Then the response should return a successful status code

  Scenario: /api/public/facilities/ responds successfully
    When I request "/api/public/facilities/"
    Then the response should return a successful status code

  Scenario: /api/public/facilities/autocomplete/ responds successfully
    When I request "/api/public/facilities/autocomplete/"
    Then the response should return a successful status code

  Scenario: /api/public/facilities/cluster responds successfully
    When I request "/api/public/facilities/cluster"
    Then the response should return a successful status code

  Scenario: /api/public/facilities/count responds successfully
    When I request "/api/public/facilities/count"
    Then the response should return a successful status code

  Scenario: /api/public/facilities/statistic responds successfully
    When I request "/api/public/facilities/statistic"
    Then the response should return a successful status code

  Scenario: /api/public/search/geoname responds successfully
    When I request "/api/public/search/geoname"
    Then the response should return a successful status code

  Scenario: /api/schema/ responds successfully
    When I request "/api/schema/"
    Then the response should return a successful status code

  Scenario: /api/v1/ responds successfully
    When I request "/api/v1/"
    Then the response should return a successful status code

  Scenario: /api/v2/ responds successfully
    When I request "/api/v2/"
    Then the response should return a successful status code

  Scenario: /api/v3/facilities/ responds successfully
    When I request "/api/v3/facilities/"
    Then the response should return a successful status code

  Scenario: /api/v3/facilities/statistic/ responds successfully
    When I request "/api/v3/facilities/statistic/"
    Then the response should return a successful status code

  Scenario: /api/v3/user/ responds successfully
    When I request "/api/v3/user/"
    Then the response should return a successful status code

  Scenario: /attributions responds successfully
    When I request "/attributions"
    Then the response should return a successful status code

  Scenario: /contact responds successfully
    When I request "/contact"
    Then the response should return a successful status code

  Scenario: /donate responds successfully
    When I request "/donate"
    Then the response should return a successful status code

  Scenario: /enrollment/form responds successfully
    When I request "/enrollment/form"
    Then the response should return a successful status code

  Scenario: /help responds successfully
    When I request "/help"
    Then the response should return a successful status code

  Scenario: /how-to-gather responds successfully
    When I request "/how-to-gather"
    Then the response should return a successful status code

  Scenario: /logout/ responds successfully
    When I request "/logout/"
    Then the response should return a successful status code

  Scenario: /map responds successfully
    When I request "/map"
    Then the response should return a successful status code

  Scenario: /profile/ responds successfully
    When I request "/profile/"
    Then the response should return a successful status code

  Scenario: /profile-update/ responds successfully
    When I request "/profile-update/"
    Then the response should return a successful status code

  Scenario: /signin/ responds successfully
    When I request "/signin/"
    Then the response should return a successful status code

  Scenario: /upload-form responds successfully
    When I request "/upload-form"
    Then the response should return a successful status code
