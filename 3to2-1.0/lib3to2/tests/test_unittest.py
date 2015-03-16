from test_all_fixers import lib3to2FixerTestCase


class Test_unittest(lib3to2FixerTestCase):
    fixer = u'unittest'

    def test_imported(self):
        b = u"import unittest"
        a = u"import unittest2"
        self.check(b, a)

    def test_used(self):
        b = u"unittest.AssertStuff(True)"
        a = u"unittest2.AssertStuff(True)"
        self.check(b, a)

    def test_from_import(self):
        b = u"from unittest import *"
        a = u"from unittest2 import *"
        self.check(b, a)

    def test_imported_from(self):
        s = u"from whatever import unittest"
        self.unchanged(s)

    def test_not_base(self):
        s = u"not_unittest.unittest.stuff()"
        self.unchanged(s)
