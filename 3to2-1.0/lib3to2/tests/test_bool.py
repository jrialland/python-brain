from test_all_fixers import lib3to2FixerTestCase


class Test_bool(lib3to2FixerTestCase):
    fixer = u"bool"

    def test_1(self):
        b = u"""
            class A:
                def __bool__(self):
                    pass
            """
        a = u"""
            class A:
                def __nonzero__(self):
                    pass
            """
        self.check(b, a)

    def test_2(self):
        b = u"""
            class A(object):
                def __bool__(self):
                    pass
            """
        a = u"""
            class A(object):
                def __nonzero__(self):
                    pass
            """
        self.check(b, a)

    def test_unchanged_1(self):
        s = u"""
            class A(object):
                def __nonzero__(self):
                    pass
            """
        self.unchanged(s)

    def test_unchanged_2(self):
        s = u"""
            class A(object):
                def __bool__(self, a):
                    pass
            """
        self.unchanged(s)

    def test_unchanged_func(self):
        s = u"""
            def __bool__(thing):
                pass
            """
        self.unchanged(s)
