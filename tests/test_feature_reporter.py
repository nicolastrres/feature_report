import io
import unittest

from hamcrest import assert_that, equal_to

import feature_reporter


class FeatureReporterTestCase(unittest.TestCase):
    def setUp(self):
        self.app = feature_reporter.app.test_client()

        self.feature_login = b'Feature: Login into social network \
            As an User\
            I want to be able to login\
            So I can share my personal information with my friends (FBI, NSA, and US government\
            Scenario: Login with valid credentials\
            Given I access to the social network home page\
            When I enter my email and password and login\
            Then I can see my beatiful picture\
            And I can see a welcome message'

        self.feature_picture = b'Feature: Post a picture \
                As an User \
                I want to be able to post a picture\
                So I can share my personal pictures with my friends (FBI, NSA, and US government\
                Scenario: Post new picture\
                Given I access to the social network home page\
                And I am logged\
                When I post a picture\
                Then I can see my beatiful picture in the timeline'

    def test_get_feature_by_default(self):
        rv = self.app.get('/')

        assert_that(200, rv.status_code)
        assert_that('Feature: Login into social network' in str(rv.data))
        assert_that('Scenario: Login with valid credential')

    def test_upload_feature(self):
        file = (io.BytesIO(self.feature_login), 'my_feature_test.feature')

        response = self.app.post('/upload', data=dict(feature_files=[file]), follow_redirects=True)

        assert_that(response.status_code, equal_to(200))
        assert_that('Feature: Login into social network' in str(response.data))

    def test_upload_mulitple_files(self):
        file1 = (io.BytesIO(self.feature_login), 'login.feature')
        file2 = (io.BytesIO(self.feature_picture), 'picture.feature')

        response = self.app.post('/upload', data=dict(feature_files=[file1, file2]), follow_redirects=True)

        assert_that(response.status_code, equal_to(200))
        assert_that('Feature: Login into social network' in str(response.data))
        assert_that('Feature: Post a picture ' in str(response.data))

    def test_upload_file_with_invalid_extension(self):
        lines = b'crazy line'
        file = (io.BytesIO(lines), 'my_feature_test.txt')

        rv = self.app.post('/upload', data=dict(feature_files=[file]), follow_redirects=True)

        assert_that(rv.status_code, equal_to(400))
        assert_that('Invalid file extension: Please only provide files with extension &#39;.feature&#39'
                    in str(rv.data))
