u"""Fixer for '{1, 2, 3}' -> 'set([1, 2, 3])'"""

from lib2to3 import fixer_base
from lib2to3.pytree import Node, Leaf
from lib2to3.pgen2 import token
from lib2to3.fixer_util import Name, LParen, RParen


def found_dict(node):
    u"""Returns true if the node is a dictionary literal (contains a colon)"""
    # node.children[1] is the dictsetmaker. none of its children may be a colon
    return any(kid.type == token.COLON for kid in node.children[1].children)


class FixSetliteral(fixer_base.BaseFix):

    PATTERN = u"""atom< '{' dictsetmaker< args=any* > '}' > |
                 atom< '{' arg=any '}' >"""

    def match(self, node):
        results = super(FixSetliteral, self).match(node)
        if results and not found_dict(node):
            return results
        else:
            return False

    def transform(self, node, results):
        syms = self.syms
        prefix = node.prefix
        args = results.get(u"args")
        arg = results.get(u"arg")
        if args:
            args = [arg.clone() for arg in args]
            args = Node(syms.atom, [Leaf(token.LSQB, u"["),
                                    Node(syms.listmaker, args),
                                    Leaf(token.RSQB, u"]")])
        elif arg:
            arg = arg.clone()
            arg = Node(syms.atom, [Leaf(token.LSQB, u"["),
                                   Node(syms.listmaker, [arg]),
                                   Leaf(token.RSQB, u"]")])
        return Node(syms.power, [Name(u"set"), LParen(), args or arg, RParen()],
                    prefix=prefix)
