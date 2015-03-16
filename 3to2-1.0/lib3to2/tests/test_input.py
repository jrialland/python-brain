from test_all_fixers import lib3to2FixerTestCase


class Test_input(lib3to2FixerTestCase):
    fixer = u"input"

    def test_prefix_preservation(self):
        b = u"""x =    input(   )"""
        a = u"""x =    raw_input(   )"""
        self.check(b, a)

        b = u"""x = input(   ''   )"""
        a = u"""x = raw_input(   ''   )"""
        self.check(b, a)

    def test_1(self):
        b = u"""x = input()"""
        a = u"""x = raw_input()"""
        self.check(b, a)

    def test_2(self):
        b = u"""x = input('a')"""
        a = u"""x = raw_input('a')"""
        self.check(b, a)

    def test_3(self):
        b = u"""x = input('prompt')"""
        a = u"""x = raw_input('prompt')"""
        self.check(b, a)

    def test_4(self):
        b = u"""x = input(foo(a) + 6)"""
        a = u"""x = raw_input(foo(a) + 6)"""
        self.check(b, a)

    def test_5(self):
        b = u"""x = input(invite).split()"""
        a = u"""x = raw_input(invite).split()"""
        self.check(b, a)

    def test_6(self):
        b = u"""x = input(invite) . split ()"""
        a = u"""x = raw_input(invite) . split ()"""
        self.check(b, a)

    def test_7(self):
        b = u"x = int(input())"
        a = u"x = int(raw_input())"
        self.check(b, a)
