from test_all_fixers import lib3to2FixerTestCase


class Test_raise(lib3to2FixerTestCase):

    fixer = u'raise'

    def test_unchanged(self):
        u"""
        Due to raise E(V) being valid in 2.5, this fixer fortunately doesn't
        need to touch code that constructs exception objects without explicit
        tracebacks.
        """

        s = u"""raise E(V)"""
        self.unchanged(s)

        s = u"""raise E("What?")"""
        self.unchanged(s)

        s = u"""raise"""
        self.unchanged(s)

    def test_what_doesnt_work(self):
        u"""
        These tests should fail, but don't.  TODO: Uncomment successfully.
        One potential way of making these work is a separate fix_exceptions
        with a lower run order than fix_raise, to communicate to fix_raise how
        to sort out that third argument.

        These items are currently outside the scope of 3to2.
        """

        b = u"""
        E = BaseException(V).with_traceback(T)
        raise E
        """

        # a = """
        #E = BaseException(V)
        #raise E, V, T
        #"""

        #self.check(b, a)
        self.unchanged(b)

        b = u"""
        E = BaseException(V)
        E.__traceback__ = S
        E.__traceback__ = T
        raise E
        """

        # a = """
        #E = BaseException(V)
        #raise E, V, T

        #self.check(b, a)
        self.unchanged(b)

    def test_traceback(self):
        u"""
        This stuff currently works, and is the opposite counterpart to the
        2to3 version of fix_raise.
        """
        b = u"""raise E(V).with_traceback(T)"""
        a = u"""raise E, V, T"""
        self.check(b, a)

        b = u"""raise E().with_traceback(T)"""
        a = u"""raise E, None, T"""
        self.check(b, a)

        b = u"""raise E("Sorry, you cannot do that.").with_traceback(T)"""
        a = u"""raise E, "Sorry, you cannot do that.", T"""
        self.check(b, a)

    def test_chain(self):
        b = u"raise E(V).with_traceback(t) from exc"
        a = u"raise E, V, t"
        self.check(b, a, ignore_warnings=True)

        b = u"raise E(V) from exc"
        a = u"raise E(V)"
        self.check(b, a, ignore_warnings=True)

        b = u"raise eBob.exception from exc"
        a = u"raise eBob.exception"
        self.check(b, a, ignore_warnings=True)
