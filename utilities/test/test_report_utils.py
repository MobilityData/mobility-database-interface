from unittest import TestCase, mock

from utilities.report_utils import clean_report


class TestCleanReport(TestCase):
    def test_clean_empty_report(self):
        test_report = {"notices": []}
        under_test = clean_report(test_report)
        self.assertEqual(under_test, {"standalone": set(), "with_filename": {}})

    def test_clean_invalid_report(self):
        test_report = {}
        self.assertRaises(Exception, clean_report, test_report)

        test_report = {"notices": [{"code_not_present": "code_not_present"}]}
        self.assertRaises(Exception, clean_report, test_report)

        test_report = {"notices": [{"code": ""}]}
        self.assertRaises(Exception, clean_report, test_report)

        test_report = {
            "notices": [{"code": "code", "notices_not_present": "notices_not_present"}]
        }
        self.assertRaises(Exception, clean_report, test_report)

        test_report = {"notices": [{"code": "code", "notices": []}]}
        self.assertRaises(Exception, clean_report, test_report)

        test_report = {"notices": [{"code": "code", "notices": [{}]}]}
        self.assertRaises(Exception, clean_report, test_report)

    def test_clean_valid_report(self):
        test_report = {
            "notices": [
                {
                    "code": "standalone",
                    "notices": [{"duplicatedField": "duplicated_field"}],
                },
                {"code": "with_filename", "notices": [{"filename": "filename"}]},
                {
                    "code": "with_child_filename",
                    "notices": [{"childFilename": "child_filename"}],
                },
            ]
        }
        under_test = clean_report(test_report)
        self.assertEqual(
            under_test,
            {
                "standalone": {"standalone"},
                "with_filename": {
                    "filename": {"with_filename"},
                    "child_filename": {"with_child_filename"},
                },
            },
        )
