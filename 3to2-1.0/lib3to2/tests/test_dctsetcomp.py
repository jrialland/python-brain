from test_all_fixers import lib3to2FixerTestCase


class Test_dctsetcomp(lib3to2FixerTestCase):
    fixer = u"dctsetcomp"

    def test_dictcomp_straightforward(self):
        b = u"{key:val for (key, val) in tuple_of_stuff}"
        a = u"dict((key, val) for (key, val) in tuple_of_stuff)"
        self.check(b, a)

    def test_dictcomp_nestedstuff_noif(self):
        b = u"{hashlify(spam):valuate(ham).whatsthis(eggs) for \
             (spam, ham, eggs) in spam_iterator}"
        a = u"dict((hashlify(spam), valuate(ham).whatsthis(eggs)) for \
             (spam, ham, eggs) in spam_iterator)"
        self.check(b, a)

    def test_dictcomp_nestedstuff_withif(self):
        b = u"{moo:(lambda new: None)(cow) for (moo, cow) in \
            farm_animal['cow'] if has_milk()}"
        a = u"dict((moo, (lambda new: None)(cow)) for (moo, cow) in \
            farm_animal['cow'] if has_milk())"
        self.check(b, a)

    def test_setcomps(self):
        u"""
        setcomp fixer should keep everything inside the same
        and only replace the {} with a set() call on a gencomp
        """
        tests = []
        tests.append(u"milk.price for milk in find_milk(store)")
        tests.append(u"compute_nth_prime(generate_complicated_thing(\
            n.value(hashlifier))) for n in my_range_func(1, (how_far+offset))")
        tests.append(u"compute_nth_prime(generate_complicated_thing(\
            n.value(hashlifier))) for n in my_range_func(1, (how_far+offset))\
            if a==b.spam()")
        for comp in tests:
            b = u"{%s}" % comp
            a = u"set(%s)" % comp
        self.check(b, a)

    def test_prefixes(self):
        b = u"spam = {foo for foo in bar}"
        a = u"spam = set(foo for foo in bar)"
        self.check(b, a)

        b = u"spam = {foo:bar for (foo, bar) in baz}"
        a = u"spam = dict((foo, bar) for (foo, bar) in baz)"
        self.check(b, a)
