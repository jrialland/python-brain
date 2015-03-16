from test_all_fixers import lib3to2FixerTestCase


class Test_fullargspec(lib3to2FixerTestCase):

    fixer = u"fullargspec"

    def test_import(self):
        b = u"from inspect import blah, blah, getfullargspec, blah, blah"
        a = u"from inspect import blah, blah, getargspec, blah, blah"
        self.warns(
            b, a, u"some of the values returned by getfullargspec are not valid in Python 2 and have no equivalent.")

    def test_usage(self):
        b = u"argspec = inspect.getfullargspec(func)"
        a = u"argspec = inspect.getargspec(func)"
        self.warns(
            b, a, u"some of the values returned by getfullargspec are not valid in Python 2 and have no equivalent.")
