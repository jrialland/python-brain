from test_all_fixers import lib3to2FixerTestCase


class Test_reduce(lib3to2FixerTestCase):
    fixer = u"reduce"

    def test_functools_import(self):

        b = u"""
            from functools import reduce
            reduce(f, it)"""
        a = u"""
            reduce(f, it)"""
        self.check(b, a)

        b = u"""
            do_other_stuff; from functools import reduce
            reduce(f, it)"""
        a = u"""
            do_other_stuff
            reduce(f, it)"""
        self.check(b, a)

        b = u"""
            do_other_stuff; from functools import reduce; do_more_stuff
            reduce(f, it)"""
        a = u"""
            do_other_stuff; do_more_stuff
            reduce(f, it)"""
        self.check(b, a)

    def test_functools_reduce(self):

        b = u"""
            import functools
            functools.reduce(spam, ['spam', 'spam', 'baked beans', 'spam'])
            """
        a = u"""
            import functools
            reduce(spam, ['spam', 'spam', 'baked beans', 'spam'])
            """
        self.check(b, a)

    def test_prefix(self):

        b = u"""
            a  =  functools.reduce( self.thing,  self.children , f( 3 ))
            """
        a = u"""
            a  =  reduce( self.thing,  self.children , f( 3 ))
            """
        self.check(b, a)
