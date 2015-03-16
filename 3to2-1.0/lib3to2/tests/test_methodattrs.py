from test_all_fixers import lib3to2FixerTestCase


class Test_methodattrs(lib3to2FixerTestCase):
    fixer = u"methodattrs"

    attrs = [u"func", u"self"]

    def test_methodattrs(self):
        for attr in self.attrs:
            b = u"a.__%s__" % attr
            a = u"a.im_%s" % attr
            self.check(b, a)

            b = u"self.foo.__%s__.foo_bar" % attr
            a = u"self.foo.im_%s.foo_bar" % attr
            self.check(b, a)

        b = u"dir(self.foo.__self__.__class__)"
        a = u"dir(self.foo.im_self.__class__)"
        self.check(b, a)

    def test_unchanged(self):
        for attr in self.attrs:
            s = u"foo(__%s__ + 5)" % attr
            self.unchanged(s)
