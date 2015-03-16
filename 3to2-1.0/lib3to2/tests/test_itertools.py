from test_all_fixers import lib3to2FixerTestCase


class Test_itertoools(lib3to2FixerTestCase):
    fixer = u"itertools"

    def test_map(self):
        b = u"""map(a, b)"""
        a = u"""from itertools import imap\nimap(a, b)"""
        self.check(b, a)

    def test_unchanged_nobuiltin(self):
        s = u"""obj.filter(a, b)"""
        self.unchanged(s)

        s = u"""
        def map():
            pass
        """
        self.unchanged(s)

    def test_filter(self):
        b = u"a =    filter( a,  b)"
        a = u"from itertools import ifilter\na =    ifilter( a,  b)"
        self.check(b, a)

    def test_zip(self):
        b = u"""for key, val in zip(a, b):\n\tdct[key] = val"""
        a = u"""from itertools import izip\nfor key, val in izip(a, b):\n\tdct[key] = val"""
        self.check(b, a)

    def test_filterfalse(self):
        b = u"""from itertools import function, filterfalse, other_function"""
        a = u"""from itertools import function, ifilterfalse, other_function"""
        self.check(b, a)

        b = u"""filterfalse(a, b)"""
        a = u"""ifilterfalse(a, b)"""
        self.check(b, a)
