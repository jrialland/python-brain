u"""
Fixer to remove class decorators
"""

from lib2to3 import fixer_base
from lib2to3.fixer_util import Call, Assign, String, Newline
from ..fixer_util import Leaf, Node, token, syms, indentation


class FixClassdecorator(fixer_base.BaseFix):

    PATTERN = u"""
              decorated < one_dec=decorator < any* > cls=classdef < 'class' name=any any* > > | 
              decorated < decorators < decs=decorator+ > cls=classdef < 'class' name=any any* > >
              """

    def transform(self, node, results):

        singleton = results.get(u"one_dec")
        classdef = results[u"cls"]
        decs = [results[u"one_dec"]] if results.get(
            u"one_dec") is not None else results[u"decs"]
        dec_strings = [unicode(dec).strip()[1:] for dec in decs]
        assign = u""
        for dec in dec_strings:
            assign += dec
            assign += u"("
        assign += results[u"name"].value
        for dec in dec_strings:
            assign += u")"
        assign = String(results[u"name"].value + u" = " + assign)
        assign_statement = Node(syms.simple_stmt, [assign, Newline()])
        prefix = None
        for dec in decs:
            if prefix is None:
                prefix = dec.prefix
            dec.remove()
        classdef.prefix = prefix
        i = indentation(node)
        pos = node.children.index(classdef) + 1
        if classdef.children[-1].children[-1].type == token.DEDENT:
            del classdef.children[-1].children[-1]
        node.insert_child(pos, Leaf(token.INDENT, i))
        node.insert_child(pos, assign_statement)
        node.insert_child(pos, Leaf(token.INDENT, i))
