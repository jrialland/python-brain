from test_all_fixers import lib3to2FixerTestCase


class Test_range(lib3to2FixerTestCase):
    fixer = u"range"

    def test_notbuiltin_list(self):
        b = u"x.list(range(10))"
        a = u"x.list(xrange(10))"
        self.check(b, a)

    def test_prefix_preservation(self):
        b = u"""x =    range(  10  )"""
        a = u"""x =    xrange(  10  )"""
        self.check(b, a)

        b = u"""x = range(  1  ,  10   )"""
        a = u"""x = xrange(  1  ,  10   )"""
        self.check(b, a)

        b = u"""x = range(  0  ,  10 ,  2 )"""
        a = u"""x = xrange(  0  ,  10 ,  2 )"""
        self.check(b, a)

    def test_single_arg(self):
        b = u"""x = range(10)"""
        a = u"""x = xrange(10)"""
        self.check(b, a)

    def test_two_args(self):
        b = u"""x = range(1, 10)"""
        a = u"""x = xrange(1, 10)"""
        self.check(b, a)

    def test_three_args(self):
        b = u"""x = range(0, 10, 2)"""
        a = u"""x = xrange(0, 10, 2)"""
        self.check(b, a)

    def test_wrapped_in_list(self):
        b = u"""x = list(range(10, 3, 9))"""
        a = u"""x = range(10, 3, 9)"""
        self.check(b, a)

        b = u"""x = foo(list(range(10, 3, 9)))"""
        a = u"""x = foo(range(10, 3, 9))"""
        self.check(b, a)

        b = u"""x = list(range(10, 3, 9)) + [4]"""
        a = u"""x = range(10, 3, 9) + [4]"""
        self.check(b, a)

        b = u"""x = list(range(10))[::-1]"""
        a = u"""x = range(10)[::-1]"""
        self.check(b, a)

        b = u"""x = list(range(10))  [3]"""
        a = u"""x = range(10)  [3]"""
        self.check(b, a)

    def test_range_in_for(self):
        b = u"""for i in range(10):\n    j=i"""
        a = u"""for i in xrange(10):\n    j=i"""
        self.check(b, a)

        b = u"""[i for i in range(10)]"""
        a = u"""[i for i in xrange(10)]"""
        self.check(b, a)
