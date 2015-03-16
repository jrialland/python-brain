from test_all_fixers import lib3to2FixerTestCase


class Test_with(lib3to2FixerTestCase):
    fixer = u"with"

    def test_with_oneline(self):
        b = u"with a as b: pass"
        a = u"from __future__ import with_statement\nwith a as b: pass"
        self.check(b, a)

    def test_with_suite(self):
        b = u"with a as b:\n    pass"
        a = u"from __future__ import with_statement\nwith a as b:\n    pass"
        self.check(b, a)
