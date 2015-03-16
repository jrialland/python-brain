from test_all_fixers import lib3to2FixerTestCase


class Test_annotations(lib3to2FixerTestCase):
    fixer = u"annotations"

    def test_return_annotations_alone(self):
        b = u"def foo() -> 'bar': pass"
        a = u"def foo(): pass"
        self.check(b, a, ignore_warnings=True)

        b = u"""
        def foo() -> "bar":
            print "baz"
            print "what's next, again?"
        """
        a = u"""
        def foo():
            print "baz"
            print "what's next, again?"
        """
        self.check(b, a, ignore_warnings=True)

    def test_single_param_annotations(self):
        b = u"def foo(bar:'baz'): pass"
        a = u"def foo(bar): pass"
        self.check(b, a, ignore_warnings=True)

        b = u"""
        def foo(bar:"baz"="spam"):
            print "what's next, again?"
            print "whatever."
        """
        a = u"""
        def foo(bar="spam"):
            print "what's next, again?"
            print "whatever."
        """
        self.check(b, a, ignore_warnings=True)

    def test_multiple_param_annotations(self):
        b = u"def foo(bar:'spam'=False, baz:'eggs'=True, ham:False='spaghetti'): pass"
        a = u"def foo(bar=False, baz=True, ham='spaghetti'): pass"
        self.check(b, a, ignore_warnings=True)

        b = u"""
        def foo(bar:"spam"=False, baz:"eggs"=True, ham:False="spam"):
            print "this is filler, just doing a suite"
            print "suites require multiple lines."
        """
        a = u"""
        def foo(bar=False, baz=True, ham="spam"):
            print "this is filler, just doing a suite"
            print "suites require multiple lines."
        """
        self.check(b, a, ignore_warnings=True)

    def test_mixed_annotations(self):
        b = u"def foo(bar=False, baz:'eggs'=True, ham:False='spaghetti') -> 'zombies': pass"
        a = u"def foo(bar=False, baz=True, ham='spaghetti'): pass"
        self.check(b, a, ignore_warnings=True)

        b = u"""
        def foo(bar:"spam"=False, baz=True, ham:False="spam") -> 'air':
            print "this is filler, just doing a suite"
            print "suites require multiple lines."
        """
        a = u"""
        def foo(bar=False, baz=True, ham="spam"):
            print "this is filler, just doing a suite"
            print "suites require multiple lines."
        """
        self.check(b, a, ignore_warnings=True)

        b = u"def foo(bar) -> 'brains': pass"
        a = u"def foo(bar): pass"
        self.check(b, a, ignore_warnings=True)

    def test_unchanged(self):
        s = u"def foo(): pass"
        self.unchanged(s)

        s = u"""
        def foo():
            pass
            pass
        """
        self.unchanged(s)

        s = u"""
        def foo(bar=baz):
            pass
            pass
        """
        self.unchanged(s)
