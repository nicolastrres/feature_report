import unittest

from hamcrest import assert_that

import feature_rerporter


class FeatureReporterTestCase(unittest.TestCase):

    def setUp(self):
        self.app = feature_rerporter.app.test_client()

    def test_get_feature_by_default(self):
        rv = self.app.get('/')
        assert_that('Feature: Login into social network' in str(rv.data))
        assert_that('Scenario: Login with valid credential')
