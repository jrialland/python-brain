from test_all_fixers import lib3to2FixerTestCase


class Test_except(lib3to2FixerTestCase):
    fixer = u"except"

    def test_prefix_preservation(self):
        a = u"""
            try:
                pass
            except (RuntimeError, ImportError),    e:
                pass"""
        b = u"""
            try:
                pass
            except (RuntimeError, ImportError) as    e:
                pass"""
        self.check(b, a)

    def test_simple(self):
        a = u"""
            try:
                pass
            except Foo, e:
                pass"""
        b = u"""
            try:
                pass
            except Foo as e:
                pass"""
        self.check(b, a)
