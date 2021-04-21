import warnings


def ignore_resource_warnings(test_func):
    """Removes the resource warnings raised by testing download execution (normal class behaviour)."""

    def test(self, *args, **kwargs):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", ResourceWarning)
            test_func(self, *args, **kwargs)

    return test
