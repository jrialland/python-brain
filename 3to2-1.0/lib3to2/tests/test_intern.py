from test_all_fixers import lib3to2FixerTestCase


class Test_intern(lib3to2FixerTestCase):
    fixer = u"intern"

    # XXX: Does not remove unused "import sys" lines.
    def test_prefix_preservation(self):
        b = u"""import sys\nx =   sys.intern(  a  )"""
        a = u"""import sys\nx =   intern(  a  )"""
        self.check(b, a)

        b = u"""import sys\ny = sys.intern("b" # test
              )"""
        a = u"""import sys\ny = intern("b" # test
              )"""
        self.check(b, a)

        b = u"""import sys\nz = sys.intern(a+b+c.d,   )"""
        a = u"""import sys\nz = intern(a+b+c.d,   )"""
        self.check(b, a)

    def test(self):
        b = u"""from sys import intern\nx = intern(a)"""
        a = u"""\nx = intern(a)"""
        self.check(b, a)

        b = u"""import sys\nz = sys.intern(a+b+c.d,)"""
        a = u"""import sys\nz = intern(a+b+c.d,)"""
        self.check(b, a)

        b = u"""import sys\nsys.intern("y%s" % 5).replace("y", "")"""
        a = u"""import sys\nintern("y%s" % 5).replace("y", "")"""
        self.check(b, a)

    # These should not be refactored

    def test_multimports(self):
        b = u"""from sys import intern, path"""
        a = u"""from sys import path"""
        self.check(b, a)

        b = u"""from sys import path, intern"""
        a = u"""from sys import path"""
        self.check(b, a)

        b = u"""from sys import argv, intern, path"""
        a = u"""from sys import argv, path"""
        self.check(b, a)

    def test_unchanged(self):
        s = u"""intern(a=1)"""
        self.unchanged(s)

        s = u"""intern(f, g)"""
        self.unchanged(s)

        s = u"""intern(*h)"""
        self.unchanged(s)

        s = u"""intern(**i)"""
        self.unchanged(s)

        s = u"""intern()"""
        self.unchanged(s)
