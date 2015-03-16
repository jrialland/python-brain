u"""
Fixer for print function to print statement

print(spam,ham,eggs,sep=sep,end=end,file=file)
->
print >>file, sep.join((str(spam),str(ham),str(eggs))),; file.write(end)
in the most complicated case.  Simpler cases:
print() -> print
print("spam") -> print "spam"
print(1,2,3) -> print 1,2,3
print(1,2,3,end=" ") -> print 1,2,3,
print(1,2,3,end="") -> print 1,2,3,; sys.stdout.write("")
print(1,2,3,file=file) -> print >>file, 1,2,3
print(1,2,3,sep=" ",end="\n") -> print 1,2,3
"""

from __future__ import with_statement  # Aiming for 2.5-compatible code

from lib2to3 import fixer_base
from lib2to3.pytree import Node, Leaf
from lib2to3.pygram import python_symbols as syms, token
from lib2to3.fixer_util import (Name, FromImport, Newline, Call, Comma, Dot,
                                LParen, RParen, touch_import)
import warnings
import sys


def gen_printargs(lst):
    u"""
    Accepts a list of all nodes in the print call's trailer.
    Yields nodes that will be easier to deal with
    """
    for node in lst:
        if node.type == syms.arglist:
            # arglist<pos=any* kwargs=(argument<"file"|"sep"|"end" "=" any>*)>
            kids = node.children
            it = kids.__iter__()
            try:
                while True:
                    arg = it.next()
                    if arg.type == syms.argument:
                        # argument < "file"|"sep"|"end" "=" (any) >
                        yield arg
                        it.next()
                    else:
                        yield arg
                        it.next()
            except StopIteration:
                continue
        else:
            yield node


def isNone(arg):
    u"""
    Returns True if arg is a None node
    """
    return arg.type == token.NAME and arg.value == u"None"


def _unicode(arg):
    u"""
    Calls unicode() on the arg in the node.
    """
    prefix = arg.prefix
    arg = arg.clone()
    arg.prefix = u""
    ret = Call(Name(u"unicode", prefix=prefix), [arg])
    return ret


def add_file_part(file, lst):
    if file is None or isNone(file):
        return
    lst.append(Leaf(token.RIGHTSHIFT, u">>", prefix=u" "))
    lst.append(file.clone())
    lst.append(Comma())


def add_sep_part(sep, pos, lst):
    if sep is not None and not isNone(sep) and \
       not (sep.type == token.STRING and sep.value in (u"' '", u'" "')):
        temp = []
        for arg in pos:
            temp.append(_unicode(arg.clone()))
            if sys.version_info >= (2, 6):
                warnings.warn(
                    u"Calling unicode() on what may be a bytes object")
            temp.append(Comma())
        del temp[-1]
        sep = sep.clone()
        sep.prefix = u" "
        args = Node(syms.listmaker, temp)
        new_list = Node(syms.atom, [Leaf(token.LSQB, u"["), args,
                                    Leaf(token.RSQB, u"]")])
        join_arg = Node(syms.trailer, [LParen(), new_list, RParen()])
        sep_join = Node(syms.power, [sep, Node(syms.trailer,
                                               [Dot(), Name(u"join")])])
        lst.append(sep_join)
        lst.append(join_arg)
    else:
        if pos:
            pos[0].prefix = u" "
        for arg in pos:
            lst.append(arg.clone())
            lst.append(Comma())
        del lst[-1]


def add_end_part(end, file, parent, loc):
    if isNone(end):
        return
    if end.type == token.STRING and end.value in (u"' '", u'" "',
                                                  u"u' '", u'u" "',
                                                  u"b' '", u'b" "'):
        return
    if file is None:
        touch_import(None, u"sys", parent)
        file = Node(syms.power, [Name(u"sys"),
                                 Node(syms.trailer, [Dot(), Name(u"stdout")])])
    end_part = Node(syms.power, [file,
                                 Node(syms.trailer, [Dot(), Name(u"write")]),
                                 Node(syms.trailer, [LParen(), end, RParen()])])
    end_part.prefix = u" "
    parent.insert_child(loc, Leaf(token.SEMI, u";"))
    parent.insert_child(loc + 1, end_part)


def replace_print(pos, opts, old_node=None):
    u"""
    Replace old_node with a new statement.
    Also hacks in the "end" functionality.
    """
    new_node = new_print(*pos, **opts)
    end = None if u"end" not in opts else opts[u"end"].clone()
    file = None if u"file" not in opts else opts[u"file"].clone()
    if old_node is None:
        parent = Node(syms.simple_stmt, [Leaf(token.NEWLINE, u"\n")])
        i = 0
    else:
        parent = old_node.parent
        i = old_node.remove()
    parent.insert_child(i, new_node)
    if end is not None and not (end.type == token.STRING and
                                end.value in (u"'\\n'", u'"\\n"')):
        add_end_part(end, file, parent, i + 1)
    return new_node


def new_print(*pos, **opts):
    u"""
    Constructs a new print_stmt node
    args is all positional arguments passed to print()
    kwargs contains zero or more of the following mappings:

    'sep': some string
    'file': some file-like object that supports the write() method
    'end': some string
    """
    children = [Name(u"print")]
    sep = None if u"sep" not in opts else opts[u"sep"]
    file = None if u"file" not in opts else opts[u"file"]
    end = None if u"end" not in opts else opts[u"end"]
    add_file_part(file, children)
    add_sep_part(sep, pos, children)
    if end is not None and not isNone(end):
        if not end.value in (u'"\\n"', u"'\\n'"):
            children.append(Comma())
    return Node(syms.print_stmt, children)


def map_printargs(args):
    u"""
    Accepts a list of all nodes in the print call's trailer.
    Returns {'pos':[all,pos,args], 'sep':sep, 'end':end, 'file':file}
    """
    printargs = [arg for arg in gen_printargs(args)]
    mapping = {}
    pos = []
    for arg in printargs:
        if arg.type == syms.argument:
            kids = arg.children
            assert kids[0].type == token.NAME, repr(arg)
            assert len(kids) > 1, repr(arg)
            assert unicode(kids[0].value) in (u"sep", u"end", u"file")
            assert unicode(kids[0].value) not in mapping, mapping
            mapping[unicode(kids[0].value)] = kids[2]
        elif arg.type == token.STAR:
            return (None, None)
        else:
            pos.append(arg)
    return (pos, mapping)


class FixPrint(fixer_base.BaseFix):

    PATTERN = u"""
              power< 'print' parens=trailer < '(' args=any* ')' > any* >
              """

    def match(self, node):
        u"""
        Since the tree needs to be fixed once and only once if and only if it
        matches, then we can start discarding matches after we make the first.
        """
        return super(FixPrint, self).match(node)

    def transform(self, node, results):
        args = results.get(u"args")
        if not args:
            parens = results.get(u"parens")
            parens.remove()
            return
        pos, opts = map_printargs(args)
        if pos is None or opts is None:
            self.cannot_convert(
                node, u"-fprint does not support argument unpacking.  fix using -xprint and then again with  -fprintfunction.")
            return
        if u"file" in opts and \
           u"end" in opts and \
           opts[u"file"].type != token.NAME:
            self.warning(opts[u"file"], u"file is not a variable name; "
                         u"print fixer suggests to bind the file to a variable "
                         u"name first before passing it to print function")
        try:
            with warnings.catch_warnings(record=True) as w:
                new_node = replace_print(pos, opts, old_node=node)
                if len(w) > 0:
                    self.warning(
                        node, u"coercing to unicode even though this may be a bytes object")
        except AttributeError:
            # Python 2.5 doesn't have warnings.catch_warnings, so we're in
            # Python 2.5 code here...
            new_node = replace_print(
                pos, dict([(str(k), opts[k]) for k in opts]), old_node=node)

        new_node.prefix = node.prefix
