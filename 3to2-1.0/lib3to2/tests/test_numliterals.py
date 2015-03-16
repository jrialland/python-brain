from test_all_fixers import lib3to2FixerTestCase


class Test_numliterals(lib3to2FixerTestCase):
    fixer = u"numliterals"

    def test_octal_1(self):
        b = u"""0o755"""
        a = u"""0755"""
        self.check(b, a)

    def test_octal_2(self):
        b = u"""0o777"""
        a = u"""0777"""
        self.check(b, a)

    def test_bin_1(self):
        b = u"""0b10010110"""
        a = u"""__builtins__.long("10010110", 2)"""
        self.check(b, a)

    def test_bin_2(self):
        b = u"""spam(0b1101011010110)"""
        a = u"""spam(__builtins__.long("1101011010110", 2))"""
        self.check(b, a)

    def test_comments_and_spacing_2(self):
        b = u"""b = 0o755 # spam"""
        a = u"""b = 0755 # spam"""
        self.check(b, a)

    def test_unchanged_str(self):
        s = u"""'0x1400'"""
        self.unchanged(s)

        s = u"""'0b011000'"""
        self.unchanged(s)

        s = u"""'0o755'"""
        self.unchanged(s)

    def test_unchanged_other(self):
        s = u"""5.0"""
        self.unchanged(s)

        s = u"""5.0e10"""
        self.unchanged(s)

        s = u"""5.4 + 4.9j"""
        self.unchanged(s)

        s = u"""4j"""
        self.unchanged(s)

        s = u"""4.4j"""
        self.unchanged(s)
