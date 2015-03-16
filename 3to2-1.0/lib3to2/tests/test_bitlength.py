from test_all_fixers import lib3to2FixerTestCase


class Test_bitlength(lib3to2FixerTestCase):
    fixer = u'bitlength'

    def test_fixed(self):
        b = u"""a = something.bit_length()"""
        a = u"""a = (len(bin(something)) - 2)"""
        self.check(b, a, ignore_warnings=True)

    def test_unfixed(self):
        s = u"""a = bit_length(fire)"""
        self.unchanged(s)

        s = u"""a = s.bit_length('some_arg')"""
        self.unchanged(s)
