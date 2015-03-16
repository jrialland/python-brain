from test_all_fixers import lib3to2FixerTestCase


class Test_funcattrs(lib3to2FixerTestCase):
    fixer = u"funcattrs"

    def test_doc_unchanged(self):
        b = u"""whats.up.__doc__"""
        self.unchanged(b)

    def test_defaults(self):
        b = u"""myFunc.__defaults__"""
        a = u"""myFunc.func_defaults"""
        self.check(b, a)

    def test_closure(self):
        b = u"""fore.__closure__"""
        a = u"""fore.func_closure"""
        self.check(b, a)

    def test_globals(self):
        b = u"""funkFunc.__globals__"""
        a = u"""funkFunc.func_globals"""
        self.check(b, a)

    def test_dict_unchanged(self):
        b = u"""tricky.__dict__"""
        self.unchanged(b)

    def test_name_unchanged(self):
        b = u"""sayMy.__name__"""
        self.unchanged(b)
