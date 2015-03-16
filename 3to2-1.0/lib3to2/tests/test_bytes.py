from test_all_fixers import lib3to2FixerTestCase


class Test_bytes(lib3to2FixerTestCase):
    fixer = u"bytes"

    def test_bytes_call_1(self):
        b = u"""bytes(x)"""
        a = u"""str(x)"""
        self.check(b, a)

    def test_bytes_call_2(self):
        b = u"""a = bytes(x) + b"florist" """
        a = u"""a = str(x) + "florist" """
        self.check(b, a)

    def test_bytes_call_noargs(self):
        b = u"""bytes()"""
        a = u"""str()"""
        self.check(b, a)

    def test_bytes_call_args_1(self):
        b = u"""bytes(x, y, z)"""
        a = u"""str(x).encode(y, z)"""
        self.check(b, a)

    def test_bytes_call_args_2(self):
        b = u"""bytes(encoding="utf-8", source="dinosaur", errors="dont-care")"""
        a = u"""str("dinosaur").encode("utf-8", "dont-care")"""
        self.check(b, a)

    def test_bytes_literal_1(self):
        b = u'''b"\x41"'''
        a = u'''"\x41"'''
        self.check(b, a)

    def test_bytes_literal_2(self):
        b = u"""b'x'"""
        a = u"""'x'"""
        self.check(b, a)

    def test_bytes_literal_3(self):
        b = u"""BR'''\x13'''"""
        a = u"""R'''\x13'''"""
        self.check(b, a)

    def test_bytes_concatenation(self):
        b = u"""b'bytes' + b'bytes'"""
        a = u"""'bytes' + 'bytes'"""
        self.check(b, a)
