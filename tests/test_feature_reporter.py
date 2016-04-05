import io
import unittest

from hamcrest import assert_that, equal_to

import feature_reporter


class FeatureReporterTestCase(unittest.TestCase):
    def setUp(self):
        self.app = feature_reporter.app.test_client()

    def test_get_feature_by_default(self):
        rv = self.app.get('/')

        assert_that(200, rv.status_code)
        assert_that('Feature: Login into social network' in str(rv.data))
        assert_that('Scenario: Login with valid credential')

    def test_upload_feature(self):
        lines = b'Feature: Login into social network \
                As an User\
                I want to be able to login\
                So I can share my personal information with my friends (FBI, NSA, and US government\
                Scenario: Login with valid credentials\
                Given I access to the social network home page\
                When I enter my email and password and login\
                Then I can see my beatiful picture\
                And I can see a welcome message'
        file = (io.BytesIO(lines), 'my_feature_test.feature')

        rv = self.app.post('/upload', data=dict(feature_file=file), follow_redirects=True)

        assert_that(rv.status_code, equal_to(200))
        assert_that('Feature: Login into social network' in str(rv.data))

    def test_upload_file_with_invalid_extension(self):
        lines = b'Feature: Login into social network \
                As an User\
                I want to be able to login\
                So I can share my personal information with my friends (FBI, NSA, and US government\
                Scenario: Login with valid credentials\
                Given I access to the social network home page\
                When I enter my email and password and login\
                Then I can see my beatiful picture\
                And I can see a welcome message'
        file = (io.BytesIO(lines), 'my_feature_test.txt')

        rv = self.app.post('/upload', data=dict(feature_file=file), follow_redirects=True)

        assert_that(rv.status_code, equal_to(400))
        assert_that('Invalid file extension: Please provide a file with an extension &#39;.feature&#39' in str(rv.data))
