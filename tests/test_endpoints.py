from tests import BaseTests
from app.endpoints import parse_notify_date


class TestEndpoints(BaseTests):
    def test_parse_notify_date_fails_if_length_is_not_3(self):
        possible_cases = ["2017-02", "", "2018/02/12", "2018-09-8-3"]

        for case in possible_cases:
            date_string, message = parse_notify_date(case)
            self.assertIsNone(date_string)
            self.assertEqual(
                message,
                "the acceptable date format is `yyyy-mm-dd`")

    def test_notify_date_fails_if_data_is_not_in_integer_form(self):
        possible_cases = ["2017-Au-13", "five-on-1"]
        for case in possible_cases:
            date_string, message = parse_notify_date(case)
            self.assertIsNone(date_string)
            self.assertEqual(
                message,
                "dates must be specified as strings but with integer values")

    def test_notify_date_fails_if_given_date_is_invalid(self):
        possible_cases = ["2017-02-30", "2017-02-31", "2018-06-31",
                          "2019-08-99"]

        for case in possible_cases:
            date_string, message = parse_notify_date(case)
            self.assertIsNone(date_string)
            self.assertEqual(
                message,
                "The given date is invalid and doesn't exist on the calendar")

    def test_notify_date_is_successful(self):
        possible_cases = ["2018-12-01", "2019-04-29", "2018-07-31"]
        for case in possible_cases:
            date_string, message = parse_notify_date(case)
            self.assertEqual(date_string, case)
            self.assertEqual(message, "success")
