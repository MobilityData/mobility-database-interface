from unittest import TestCase
from utilities.validators import (
    is_valid_instance,
    is_valid_str,
    is_valid_int,
    is_valid_list,
    is_valid_dict,
)


class TestInstanceValidators(TestCase):
    def test_is_valid_instance_with_valid_instance(self):
        test_prop_instance = "test_prop_instance"
        test_prop_class = str
        under_test = is_valid_instance(test_prop_instance, test_prop_class)
        self.assertTrue(under_test)

    def test_is_valid_instance_with_falsy_instance(self):
        test_prop_instance = ""
        test_prop_class = str
        under_test = is_valid_instance(test_prop_instance, test_prop_class)
        self.assertFalse(under_test)

    def test_is_valid_instance_with_invalid_instance(self):
        test_prop_instance = 0
        test_prop_class = str
        under_test = is_valid_instance(test_prop_instance, test_prop_class)
        self.assertFalse(under_test)

    def test_is_valid_str_with_valid_str(self):
        test_prop_instance = "test_prop_instance"
        under_test = is_valid_str(test_prop_instance)
        self.assertTrue(under_test)

    def test_is_valid_str_with_falsy_str(self):
        test_prop_instance = ""
        under_test = is_valid_str(test_prop_instance)
        self.assertFalse(under_test)

    def test_is_valid_str_with_invalid_str(self):
        test_prop_instance = 0
        under_test = is_valid_str(test_prop_instance)
        self.assertFalse(under_test)

    def test_is_valid_int_with_valid_int(self):
        test_prop_instance = 1
        under_test = is_valid_int(test_prop_instance)
        self.assertTrue(under_test)

    def test_is_valid_int_with_falsy_int(self):
        test_prop_instance = 0
        under_test = is_valid_int(test_prop_instance)
        self.assertFalse(under_test)

    def test_is_valid_int_with_invalid_int(self):
        test_prop_instance = ""
        under_test = is_valid_int(test_prop_instance)
        self.assertFalse(under_test)

    def test_is_valid_list_with_valid_list(self):
        test_prop_instance = ["test_list"]
        under_test = is_valid_list(test_prop_instance)
        self.assertTrue(under_test)

    def test_is_valid_list_with_falsy_list(self):
        test_prop_instance = []
        under_test = is_valid_list(test_prop_instance)
        self.assertFalse(under_test)

    def test_is_valid_list_with_invalid_list(self):
        test_prop_instance = ""
        under_test = is_valid_list(test_prop_instance)
        self.assertFalse(under_test)

    def test_is_valid_dict_with_valid_dict(self):
        test_prop_instance = {"test_key": "test_value"}
        under_test = is_valid_dict(test_prop_instance)
        self.assertTrue(under_test)

    def test_is_valid_dict_with_falsy_dict(self):
        test_prop_instance = {}
        under_test = is_valid_dict(test_prop_instance)
        self.assertFalse(under_test)

    def test_is_valid_dict_with_invalid_dict(self):
        test_prop_instance = ""
        under_test = is_valid_dict(test_prop_instance)
        self.assertFalse(under_test)
