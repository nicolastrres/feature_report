from hamcrest import assert_that, equal_to, has_length

from application.feature_file_parser.parse_feature_files import get_feature, get_scenarios


def test_get_feature_from_file():
    feature = get_feature('test.feature')
    assert_that(feature, equal_to('Feature: Login into social network'))


def test_get_scenarios():
    expected_scenario_1 = 'Scenario: Login with valid credentials\n' \
                          'Given I access to the social network home page\n' \
                          'When I enter my email and password and login\n' \
                          'Then I can see my beatiful picture\n' \
                          'And I can see a welcome message\n\n'

    expected_scenario_2 = 'Scenario: Not possible to login with invalid credentials\n' \
                          'Given I have invalid credentials\n' \
                          'When I enter my email and password\n' \
                          'And try to login\n' \
                          'Then I cannot see my beatiful picture\n' \
                          'And I get an error message\n'

    with open('test.feature') as file:
        file_lines = file.readlines()
        scenarios = get_scenarios(file_lines)

        assert_that(scenarios, has_length(2))
        assert_that(scenarios[0], equal_to(expected_scenario_1))
        assert_that(scenarios[1], equal_to(expected_scenario_2))
