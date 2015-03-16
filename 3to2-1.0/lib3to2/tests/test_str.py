from test_all_fixers import lib3to2FixerTestCase


class Test_str(lib3to2FixerTestCase):
    fixer = u"str"

    def test_str_call(self):
        b = u"""str(x, y, z)"""
        a = u"""unicode(x, y, z)"""
        self.check(b, a)

    def test_chr_call(self):
        b = u"""chr(a, t, m)"""
        a = u"""unichr(a, t, m)"""
        self.check(b, a)

    def test_str_literal_1(self):
        b = u'''"x"'''
        a = u'''u"x"'''
        self.check(b, a)

    def test_str_literal_2(self):
        b = u"""r'x'"""
        a = u"""ur'x'"""
        self.check(b, a)

    def test_str_literal_3(self):
        b = u"""R'''x'''"""
        a = u"""uR'''x'''"""
        self.check(b, a)
