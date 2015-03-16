from test_all_fixers import lib3to2FixerTestCase


class Test_collections(lib3to2FixerTestCase):
    fixer = u"collections"

    def test_from_UserDict(self):

        b = u"""
        from collections import UserDict"""
        a = u"""
        from UserDict import UserDict"""
        self.check(b, a)

    def test_from_UserList(self):

        b = u"""
        from collections import UserList"""
        a = u"""
        from UserList import UserList"""
        self.check(b, a)

    def test_from_UserString(self):

        b = u"""
        from collections import UserString"""
        a = u"""
        from UserString import UserString"""
        self.check(b, a)

    def test_using_UserDict(self):

        b = u"""
        class Scapegoat(collections.UserDict):
            pass"""
        a = u"""import UserDict

class Scapegoat(UserDict.UserDict):
    pass"""
        self.check(b, a)

    def test_using_UserList(self):

        b = u"""
        class Scapegoat(collections.UserList):
            pass"""
        a = u"""import UserList

class Scapegoat(UserList.UserList):
    pass"""
        self.check(b, a)

    def test_using_UserString(self):

        b = u"""
        class Scapegoat(collections.UserString):
            pass"""
        a = u"""import UserString

class Scapegoat(UserString.UserString):
    pass"""
        self.check(b, a)
