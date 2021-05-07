from unittest import TestCase
from utilities.validators import (
    is_valid_instance,
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

    def test_is_valid_instance_with_none_instance(self):
        test_prop_instance = None
        test_prop_class = str
        under_test = is_valid_instance(test_prop_instance, test_prop_class)
        self.assertFalse(under_test)

    def test_is_valid_instance_with_false_instance(self):
        test_prop_instance = False
        test_prop_class = str
        under_test = is_valid_instance(test_prop_instance, test_prop_class)
        self.assertFalse(under_test)
