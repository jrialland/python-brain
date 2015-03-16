from test_all_fixers import lib3to2FixerTestCase
from itertools import count


class Test_division(lib3to2FixerTestCase):
    fixer = u"division"

    counter = count(1)
    divisions = [(u"1", u"2"),
                 (u"spam", u"eggs"),
                 (u"lambda a: a(4)", u"my_foot(your_face)"),
                 (u"temp(bob)", u"4"),
                 (u"29.4", u"green()")]

    for top, bottom in divisions:
        exec(u"def test_%d(self):\n    b = \"%s/%s\"\n    a = \"from __future__ import division\\n%s/%s\"\n    self.check(b, a)" %
             (counter.next(), top, bottom, top, bottom))
