from test_all_fixers import lib3to2FixerTestCase


class Test_printfunction(lib3to2FixerTestCase):
    fixer = u"printfunction"

    def test_generic(self):
        b = u"""print()"""
        a = u"""from __future__ import print_function\nprint()"""
        self.check(b, a)

    def test_literal(self):
        b = u"""print('spam')"""
        a = u"""from __future__ import print_function\nprint('spam')"""
        self.check(b, a)

    def test_not_builtin_unchanged(self):
        s = u"this.shouldnt.be.changed.because.it.isnt.builtin.print()"
        self.unchanged(s)

    # XXX: Quoting this differently than triple-quotes, because with newline
    # XXX: setting, I can't quite get the triple-quoted versions to line up.
    def test_arbitrary_printing(self):
        b = u"import dinosaur.skull\nimport sys\nprint"\
            u"(skull.jaw, skull.jaw.biteforce, file=sys.stderr)"
        a = u"from __future__ import print_function\n"\
            u"import dinosaur.skull\nimport sys\nprint"\
            u"(skull.jaw, skull.jaw.biteforce, file=sys.stderr)"
        self.check(b, a)

    def test_long_arglist(self):
        b = u"print(spam, spam, spam, spam, spam, baked_beans, spam, spam,"\
            u"spam, spam, sep=', spam, ', end=wonderful_spam)\nprint()"
        a = u"from __future__ import print_function\n"\
            u"print(spam, spam, spam, spam, spam, baked_beans, spam, spam,"\
            u"spam, spam, sep=', spam, ', end=wonderful_spam)\nprint()"
        self.check(b, a)
