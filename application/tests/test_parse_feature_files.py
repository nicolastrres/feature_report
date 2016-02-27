from hamcrest import assert_that, equal_to
from application.feature_file_parser.parse_feature_files import get_feature


def test_get_feature_from_file():
    feature = get_feature('test.feature')
    assert_that(feature, equal_to('Feature: Login into social network'))
