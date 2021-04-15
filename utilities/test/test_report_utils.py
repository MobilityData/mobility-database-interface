from unittest import TestCase, mock

from utilities.report_utils import clean_report, merge_reports


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
                    "code": "standalone_notice",
                    "notices": [{"duplicatedField": "duplicated_field"}],
                },
                {"code": "with_filename_notice", "notices": [{"filename": "filename"}]},
                {
                    "code": "with_child_filename_notice",
                    "notices": [{"childFilename": "child_filename"}],
                },
            ]
        }
        under_test = clean_report(test_report)
        self.assertEqual(
            under_test,
            {
                "standalone": {"standalone_notice"},
                "with_filename": {
                    "filename": {"with_filename_notice"},
                    "child_filename": {"with_child_filename_notice"},
                },
            },
        )


class TestMergeReports(TestCase):
    def test_merge_empty_reports(self):
        test_validation_report = {"standalone": set(), "with_filename": {}}
        test_system_report = {"standalone": set(), "with_filename": {}}
        under_test = merge_reports(test_validation_report, test_system_report)
        self.assertEqual(under_test, {"standalone": set(), "with_filename": {}})

    def test_merge_reports(self):
        test_validation_report = {
            "standalone": {"standalone_validation_notice"},
            "with_filename": {
                "filename": {"with_filename_validation_notice"},
                "child_filename": {"with_child_filename_validation_notice"},
                "another_filename_validation": {"another_validation_filename_notice"},
            },
        }
        test_system_report = {
            "standalone": {"standalone_system_notice"},
            "with_filename": {
                "filename": {"with_filename_system_notice"},
                "child_filename": {"with_child_filename_system_notice"},
                "another_filename_system": {"another_system_filename_notice"},
            },
        }
        under_test = merge_reports(test_validation_report, test_system_report)
        self.assertEqual(
            under_test,
            {
                "standalone": {
                    "standalone_system_notice",
                    "standalone_validation_notice",
                },
                "with_filename": {
                    "filename": {
                        "with_filename_system_notice",
                        "with_filename_validation_notice",
                    },
                    "another_filename_validation": {
                        "another_validation_filename_notice"
                    },
                    "child_filename": {
                        "with_child_filename_validation_notice",
                        "with_child_filename_system_notice",
                    },
                    "another_filename_system": {"another_system_filename_notice"},
                },
            },
        )
