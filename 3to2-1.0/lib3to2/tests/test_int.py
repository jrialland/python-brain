from test_all_fixers import lib3to2FixerTestCase


class Test_int(lib3to2FixerTestCase):
    fixer = u"int"

    def test_1(self):
        b = u"""x = int(x)"""
        a = u"""x = long(x)"""
        self.check(b, a)

    def test_2(self):
        b = u"""y = isinstance(x, int)"""
        a = u"""y = isinstance(x, long)"""
        self.check(b, a)

    def test_unchanged(self):
        s = u"""int = True"""
        self.unchanged(s)

        s = u"""s.int = True"""
        self.unchanged(s)

        s = u"""def int(): pass"""
        self.unchanged(s)

        s = u"""class int(): pass"""
        self.unchanged(s)

        s = u"""def f(int): pass"""
        self.unchanged(s)

        s = u"""def f(g, int): pass"""
        self.unchanged(s)

        s = u"""def f(x, int=True): pass"""
        self.unchanged(s)

    def test_prefix_preservation(self):
        b = u"""x =   int(  x  )"""
        a = u"""x =   long(  x  )"""
        self.check(b, a)

    def test_literal_1(self):
        b = u"""5"""
        a = u"""5L"""
        self.check(b, a)

    def test_literal_2(self):
        b = u"""a = 12"""
        a = u"""a = 12L"""
        self.check(b, a)

    def test_literal_3(self):
        b = u"""0"""
        a = u"""0L"""
        self.check(b, a)

    def test_complex_1(self):
        b = u"""5 + 4j"""
        a = u"""5L + 4j"""
        self.check(b, a)

    def test_complex_2(self):
        b = u"""35  +  2j"""
        a = u"""35L  +  2j"""
        self.check(b, a)
