from test_all_fixers import lib3to2FixerTestCase


class Test_next(lib3to2FixerTestCase):
    fixer = u"next"

    def test_1(self):
        b = u"""next(it)"""
        a = u"""it.next()"""
        self.check(b, a)

    def test_2(self):
        b = u"""next(a.b.c.d)"""
        a = u"""a.b.c.d.next()"""
        self.check(b, a)

    def test_3(self):
        b = u"""next((a + b))"""
        a = u"""(a + b).next()"""
        self.check(b, a)

    def test_4(self):
        b = u"""next(a())"""
        a = u"""a().next()"""
        self.check(b, a)

    def test_5(self):
        b = u"""next(a()) + b"""
        a = u"""a().next() + b"""
        self.check(b, a)

    def test_6(self):
        b = u"""c(      next(a()) + b)"""
        a = u"""c(      a().next() + b)"""
        self.check(b, a)

    def test_prefix_preservation_1(self):
        b = u"""
            for a in b:
                foo(a)
                next(a)
            """
        a = u"""
            for a in b:
                foo(a)
                a.next()
            """
        self.check(b, a)

    def test_prefix_preservation_2(self):
        b = u"""
            for a in b:
                foo(a) # abc
                # def
                next(a)
            """
        a = u"""
            for a in b:
                foo(a) # abc
                # def
                a.next()
            """
        self.check(b, a)

    def test_prefix_preservation_3(self):
        b = u"""
            next = 5
            for a in b:
                foo(a)
                a.__next__()
            """

        a = u"""
            next = 5
            for a in b:
                foo(a)
                a.next()
            """
        self.check(b, a)

    def test_prefix_preservation_4(self):
        b = u"""
            next = 5
            for a in b:
                foo(a) # abc
                # def
                a.__next__()
            """
        a = u"""
            next = 5
            for a in b:
                foo(a) # abc
                # def
                a.next()
            """
        self.check(b, a)

    def test_prefix_preservation_5(self):
        b = u"""
            next = 5
            for a in b:
                foo(foo(a), # abc
                    a.__next__())
            """
        a = u"""
            next = 5
            for a in b:
                foo(foo(a), # abc
                    a.next())
            """
        self.check(b, a)

    def test_prefix_preservation_6(self):
        b = u"""
            for a in b:
                foo(foo(a), # abc
                    next(a))
            """
        a = u"""
            for a in b:
                foo(foo(a), # abc
                    a.next())
            """
        self.check(b, a)

    def test_method_1(self):
        b = u"""
            class A:
                def __next__(self):
                    pass
            """
        a = u"""
            class A:
                def next(self):
                    pass
            """
        self.check(b, a)

    def test_method_2(self):
        b = u"""
            class A(object):
                def __next__(self):
                    pass
            """
        a = u"""
            class A(object):
                def next(self):
                    pass
            """
        self.check(b, a)

    def test_method_3(self):
        b = u"""
            class A:
                def __next__(x):
                    pass
            """
        a = u"""
            class A:
                def next(x):
                    pass
            """
        self.check(b, a)

    def test_method_4(self):
        b = u"""
            class A:
                def __init__(self, foo):
                    self.foo = foo

                def __next__(self):
                    pass

                def __iter__(self):
                    return self
            """
        a = u"""
            class A:
                def __init__(self, foo):
                    self.foo = foo

                def next(self):
                    pass

                def __iter__(self):
                    return self
            """
        self.check(b, a)

    def test_noncall_access_1(self):
        b = u"""gnext = g.__next__"""
        a = u"""gnext = g.next"""
        self.check(b, a)

    def test_noncall_access_2(self):
        b = u"""f(g.__next__ + 5)"""
        a = u"""f(g.next + 5)"""
        self.check(b, a)

    def test_noncall_access_3(self):
        b = u"""f(g().__next__ + 5)"""
        a = u"""f(g().next + 5)"""
        self.check(b, a)
