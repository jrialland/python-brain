from test_all_fixers import lib3to2FixerTestCase


class Test_setliteral(lib3to2FixerTestCase):
    fixer = u"setliteral"

    def test_unchanged_dict(self):
        s = u"""{"ghoul": 100, "zombie": 50, "gremlin": 40}"""
        self.unchanged(s)

        s = u"""{1: "spider", 2: "hills", 3: "bologna", None: "tapeworm"}"""
        self.unchanged(s)

        s = u"""{}"""
        self.unchanged(s)

        s = u"""{'a':'b'}"""
        self.unchanged(s)

    def test_simple_literal(self):
        b = u"""{'Rm 101'}"""
        a = u"""set(['Rm 101'])"""
        self.check(b, a)

    def test_multiple_items(self):
        b = u"""{'Rm 101',   'Rm 102',  spam,    ham,      eggs}"""
        a = u"""set(['Rm 101',   'Rm 102',  spam,    ham,      eggs])"""
        self.check(b, a)

        b = u"""{ a,  b,   c,    d,     e}"""
        a = u"""set([ a,  b,   c,    d,     e])"""
        self.check(b, a)

    def test_simple_set_comprehension(self):
        b = u"""{x for x in range(256)}"""
        a = u"""set([x for x in range(256)])"""
        self.check(b, a)

    def test_complex_set_comprehension(self):
        b = u"""{F(x) for x in range(256) if x%2}"""
        a = u"""set([F(x) for x in range(256) if x%2])"""
        self.check(b, a)

        b = u"""{(lambda x: 2000 + x)(x) for x, y in {(5, 400), (6, 600), (7, 900), (8, 1125), (9, 1000)}}"""
        a = u"""set([(lambda x: 2000 + x)(x) for x, y in set([(5, 400), (6, 600), (7, 900), (8, 1125), (9, 1000)])])"""
        self.check(b, a)
