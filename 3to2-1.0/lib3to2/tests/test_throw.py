from test_all_fixers import lib3to2FixerTestCase


class Test_throw(lib3to2FixerTestCase):

    fixer = u'throw'

    def test_unchanged(self):
        u"""
        Due to g.throw(E(V)) being valid in 2.5, this fixer fortunately doesn't
        need to touch code that constructs exception objects without explicit
        tracebacks.
        """

        s = u"""g.throw(E(V))"""
        self.unchanged(s)

        s = u"""omg.throw(E("What?"))"""
        self.unchanged(s)

    def test_what_doesnt_work(self):
        u"""
        These tests should fail, but don't.  TODO: Uncomment successfully.
        One potential way of making these work is a separate fix_exceptions
        with a lower run order than fix_throw, to communicate to fix_throw how
        to sort out that third argument.

        These items are currently outside the scope of 3to2.
        """

        b = u"""
        E = BaseException(V).with_traceback(T)
        gen.throw(E)
        """

        # a = """
        #E = BaseException(V)
        #gen.throw(E, V, T)
        #"""

        #self.check(b, a)
        self.unchanged(b)

        b = u"""
        E = BaseException(V)
        E.__traceback__ = S
        E.__traceback__ = T
        gen.throw(E)
        """

        # a = """
        #E = BaseException(V)
        #gen.throw(E, V, T)

        #self.check(b, a)
        self.unchanged(b)

    def test_traceback(self):
        u"""
        This stuff currently works, and is the opposite counterpart to the
        2to3 version of fix_throw.
        """
        b = u"""myGen.throw(E(V).with_traceback(T))"""
        a = u"""myGen.throw(E, V, T)"""
        self.check(b, a)

        b = u"""fling.throw(E().with_traceback(T))"""
        a = u"""fling.throw(E, None, T)"""
        self.check(b, a)

        b = u"""myVar.throw(E("Sorry, you cannot do that.").with_traceback(T))"""
        a = u"""myVar.throw(E, "Sorry, you cannot do that.", T)"""
        self.check(b, a)
