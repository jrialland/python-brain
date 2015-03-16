from test_all_fixers import lib3to2FixerTestCase


class Test_super(lib3to2FixerTestCase):
    fixer = u"super"

    def test_noargs(self):

        b = u"def m(self):\n    super()"
        a = u"def m(self):\n    super(self.__class__, self)"
        self.check(b, a)

    def test_other_params(self):

        b = u"def m(a, self=None):\n    super()"
        a = u"def m(a, self=None):\n    super(a.__class__, a)"
        self.check(b, a)

    def test_no_with_stars(self):

        s = u"def m(*args, **kwargs):\n    super()"
        self.unchanged(s, ignore_warnings=True)

    def test_no_with_noargs(self):

        s = u"def m():\n    super()"
        self.unchanged(s, ignore_warnings=True)
