from test_all_fixers import lib3to2FixerTestCase


class Test_print(lib3to2FixerTestCase):
    fixer = u"print"

    def test_generic(self):
        b = u"""print()"""
        a = u"""print"""
        self.check(b, a)

    def test_literal(self):
        b = u"""print('spam')"""
        a = u"""print 'spam'"""
        self.check(b, a)

    def test_not_builtin_unchanged(self):
        s = u"this.shouldnt.be.changed.because.it.isnt.builtin.print()"
        self.unchanged(s)

    # XXX: Quoting this differently than triple-quotes, because with newline
    # XXX: setting, I can't quite get the triple-quoted versions to line up.
    def test_arbitrary_printing(self):
        b = u"import dinosaur.skull\nimport sys\nprint"\
            u"(skull.jaw, skull.jaw.biteforce, file=sys.stderr)"
        a = u"import dinosaur.skull\nimport sys\nprint "\
            u">>sys.stderr, skull.jaw, skull.jaw.biteforce"
        self.check(b, a)

    def test_long_arglist(self):
        b = u"print(spam, spam, spam, spam, spam, baked_beans, spam, spam,"\
            u" spam, spam, sep=', spam, ', end=wonderful_spam)\nprint()"
        a = u"import sys\nprint ', spam, '.join([unicode(spam), unicode(spam), unicode(spam), unicode(spam), unicode(spam), unicode(baked_beans),"\
            u" unicode(spam), unicode(spam), unicode(spam), unicode(spam)]),; sys.stdout.write(wonderful_spam)\nprint"
        self.check(b, a, ignore_warnings=True)

    def test_nones(self):
        b = u"print(1,2,3,end=None, sep=None, file=None)"
        a = u"print 1,2,3"
        self.check(b, a)

    def test_argument_unpacking(self):
        s = u"print(*args)"
        self.warns_unchanged(
            s, u"-fprint does not support argument unpacking.  fix using -xprint and then again with  -fprintfunction.")
