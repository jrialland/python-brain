from test_all_fixers import lib3to2FixerTestCase


class Test_getcwd(lib3to2FixerTestCase):
    fixer = u"getcwd"

    def test_prefix_preservation(self):
        b = u"""ls =    os.listdir(  os.getcwd()  )"""
        a = u"""ls =    os.listdir(  os.getcwdu()  )"""
        self.check(b, a)

        b = u"""whatdir = os.getcwd      (      )"""
        a = u"""whatdir = os.getcwdu      (      )"""
        self.check(b, a)
