u"""
Fixer for:
anything.bit_length() -> (len(bin(anything)) - 2)
"""

from lib2to3 import fixer_base
from ..fixer_util import LParen, RParen, Call, Number, Name, Minus, Node, syms


class FixBitlength(fixer_base.BaseFix):

    PATTERN = u"power< name=any trailer< '.' 'bit_length' > trailer< '(' ')' > >"

    def transform(self, node, results):

        name = results[u"name"]
        inner = Call(Name(u"bin"), [Name(name.value)])
        outer = Call(Name(u"len"), [inner])
        middle = Minus(prefix=u" ")
        two = Number(u"2", prefix=u" ")
        node.replace(
            Node(syms.power, [LParen(), outer, middle, two, RParen()], prefix=node.prefix))
