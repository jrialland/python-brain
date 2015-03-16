from test_all_fixers import lib3to2FixerTestCase


class Test_open(lib3to2FixerTestCase):
    fixer = u"open"

    def test_imports(self):
        b = u"""new_file = open("some_filename", newline="\\r")"""
        a = u"""from io import open\nnew_file = open("some_filename", newline="\\r")"""
        self.check(b, a)

    def test_doesnt_import(self):
        s = u"""new_file = nothing.open("some_filename")"""
        self.unchanged(s)
