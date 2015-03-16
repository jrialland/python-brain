from test_all_fixers import lib3to2FixerTestCase


class Test_memoryview(lib3to2FixerTestCase):
    fixer = u"memoryview"

    def test_simple(self):
        b = u"""x = memoryview(y)"""
        a = u"""x = buffer(y)"""
        self.check(b, a)

    def test_slicing(self):
        b = u"""x = memoryview(y)[1:4]"""
        a = u"""x = buffer(y)[1:4]"""
        self.check(b, a)

    def test_prefix_preservation(self):
        b = u"""x =       memoryview(  y )[1:4]"""
        a = u"""x =       buffer(  y )[1:4]"""
        self.check(b, a)

    def test_nested(self):
        b = u"""x = list(memoryview(y)[1:4])"""
        a = u"""x = list(buffer(y)[1:4])"""
        self.check(b, a)
