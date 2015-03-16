u"""
Fixer for bytes -> str.
"""

import re
from lib2to3 import fixer_base
from lib2to3.patcomp import compile_pattern
from ..fixer_util import Name, token, syms, parse_args, Call, Comma

_literal_re = re.compile(ur"[bB][rR]?[\'\"]")


class FixBytes(fixer_base.BaseFix):

    order = u"pre"

    PATTERN = u"STRING | power< 'bytes' [trailer< '(' (args=arglist | any*) ')' >] > | 'bytes'"

    def transform(self, node, results):
        name = results.get(u"name")
        arglist = results.get(u"args")
        if node.type == token.NAME:
            return Name(u"str", prefix=node.prefix)
        elif node.type == token.STRING:
            if _literal_re.match(node.value):
                new = node.clone()
                new.value = new.value[1:]
                return new
        if arglist is not None:
            args = arglist.children
            parsed = parse_args(args, (u"source", u"encoding", u"errors"))

            source, encoding, errors = (
                parsed[v] for v in (u"source", u"encoding", u"errors"))
            encoding.prefix = u""
            str_call = Call(Name(u"str"), ([source.clone()]))
            if errors is None:
                node.replace(
                    Call(Name(unicode(str_call) + u".encode"), (encoding.clone(),)))
            else:
                errors.prefix = u" "
                node.replace(Call(Name(
                    unicode(str_call) + u".encode"), (encoding.clone(), Comma(), errors.clone())))
