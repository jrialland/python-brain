from test_all_fixers import lib3to2FixerTestCase


class Test_imports(lib3to2FixerTestCase):
    fixer = u"imports"

    def test_various_unchanged(self):

        # Enclosed in a string
        s = u"'import queue'"
        self.unchanged(s)

        # Never was imported
        s = u"print(queue)"
        self.unchanged(s)

    def test_all_nodotted_names_solo(self):

        b = u"import configparser"
        a = u"import ConfigParser"
        self.check(b, a)

        b = u"from winreg import *"
        a = u"from _winreg import *"
        self.check(b, a)

        b = u"import copyreg"
        a = u"import copy_reg"
        self.check(b, a)

        b = u"import queue"
        a = u"import Queue"
        self.check(b, a)

        b = u"import socketserver"
        a = u"import SocketServer"
        self.check(b, a)

        b = u"import _markupbase"
        a = u"import markupbase"
        self.check(b, a)

        b = u"import builtins"
        a = u"import __builtin__"
        self.check(b, a)

    def test_nodotted_names_duo(self):

        b = u"import configparser, copyreg"
        a = u"import ConfigParser, copy_reg"
        self.check(b, a)

        b = u"import _markupbase, queue as bob"
        a = u"import markupbase, Queue as bob"
        self.check(b, a)

        b = u"import socketserver, builtins"
        a = u"import SocketServer, __builtin__"
        self.check(b, a)

    def test_nodotted_names_quad(self):

        b = u"import configparser, winreg, socketserver, _markupbase"
        a = u"import ConfigParser, _winreg, SocketServer, markupbase"
        self.check(b, a)

        b = u"import queue, math, _markupbase, copyreg"
        a = u"import Queue, math, markupbase, copy_reg"
        self.check(b, a)

    def test_all_dotted_names_solo(self):

        b = u"import dbm.bsd as bsd"
        a = u"import dbhash as bsd"
        self.check(b, a)

        b = u"import dbm.ndbm"
        a = u"import dbm"
        self.check(b, a)

        b = u"import dbm.dumb"
        a = u"import dumbdbm"
        self.check(b, a)

        b = u"from dbm import gnu"
        a = u"import gdbm as gnu"
        self.check(b, a)

        b = u"import html.parser"
        a = u"import HTMLParser"
        self.check(b, a)

        b = u"import html.entities"
        a = u"import htmlentitydefs"
        self.check(b, a)

        b = u"from http import client"
        a = u"import httplib as client"
        self.check(b, a)

        b = u"import http.cookies"
        a = u"import Cookie"
        self.check(b, a)

        b = u"import http.cookiejar"
        a = u"import cookielib"
        self.check(b, a)

        b = u"import tkinter.dialog"
        a = u"import Dialog"
        self.check(b, a)

        b = u"import tkinter._fix"
        a = u"import FixTk"
        self.check(b, a)

        b = u"import tkinter.scrolledtext"
        a = u"import ScrolledText"
        self.check(b, a)

        b = u"import tkinter.tix"
        a = u"import Tix"
        self.check(b, a)

        b = u"import tkinter.constants"
        a = u"import Tkconstants"
        self.check(b, a)

        b = u"import tkinter.dnd"
        a = u"import Tkdnd"
        self.check(b, a)

        b = u"import tkinter.__init__"
        a = u"import Tkinter"
        self.check(b, a)

        # TODO: Make this work (see the fix_imports)
        #b = "import tkinter"
        #a = "import Tkinter"
        #self.check(b, a)

        b = u"import tkinter.colorchooser"
        a = u"import tkColorChooser"
        self.check(b, a)

        b = u"import tkinter.commondialog"
        a = u"import tkCommonDialog"
        self.check(b, a)

        b = u"from tkinter.font import *"
        a = u"from tkFont import *"
        self.check(b, a)

        b = u"import tkinter.messagebox"
        a = u"import tkMessageBox"
        self.check(b, a)

        b = u"import tkinter.turtle"
        a = u"import turtle"
        self.check(b, a)

        b = u"import urllib.robotparser"
        a = u"import robotparser"
        self.check(b, a)

        b = u"import test.support"
        a = u"import test.test_support"
        self.check(b, a)

        b = u"from test import support"
        a = u"from test import test_support as support"
        self.check(b, a)

        b = u"import xmlrpc.client"
        a = u"import xmlrpclib"
        self.check(b, a)

        b = u"from test import support as spam, not_support as not_spam"
        a = u"from test import test_support as spam, not_support as not_spam"
        self.check(b, a)

    def test_dotted_names_duo(self):

        b = u"import   tkinter.font,  dbm.bsd"
        a = u"import   tkFont,  dbhash"
        self.check(b, a)

        b = u"import test.support,  http.cookies"
        a = u"import test.test_support,  Cookie"
        self.check(b, a)

    def test_from_import(self):

        b = u"from test.support import things"
        a = u"from test.test_support import things"
        self.check(b, a)

        b = u"from builtins import open"
        a = u"from __builtin__ import open"
        self.check(b, a)

    def test_dotted_names_quad(self):

        b = u"import    html.parser as spam,  math,     tkinter.__init__,   dbm.gnu #comment!"
        a = u"import    HTMLParser as spam,  math,     Tkinter,   gdbm #comment!"
        self.check(b, a)

        b = u"import math, tkinter.dnd, dbm.ndbm as one, dbm.ndbm as two, urllib"
        a = u"import math, Tkdnd, dbm as one, dbm as two, urllib"
        self.check(b, a)

    def test_usage(self):

        b = u"""
        import queue as james
        james.do_stuff()"""
        a = u"""
        import Queue as james
        james.do_stuff()"""
        self.check(b, a)

        b = u"""
        import queue
        queue.do_stuff()"""
        a = u"""
        import Queue
        Queue.do_stuff()"""
        self.check(b, a)

        b = u"""
        import dbm.gnu
        dbm.gnu.open('generic_file')"""
        a = u"""
        import gdbm
        gdbm.open('generic_file')"""
        self.check(b, a)

        b = u"""
        import tkinter.dialog, tkinter.colorchooser
        tkinter = tkinter.dialog(tkinter.colorchooser("Just messing around"))
        tkinter.test_should_work = True
        tkinter.dialog.dont.code.like.this = True"""
        a = u"""
        import Dialog, tkColorChooser
        tkinter = Dialog(tkColorChooser("Just messing around"))
        tkinter.test_should_work = True
        Dialog.dont.code.like.this = True"""
        self.check(b, a)

        b = u"""
        open = bob
        import builtins
        myOpen = builtins.open"""
        a = u"""
        open = bob
        import __builtin__
        myOpen = __builtin__.open"""
        self.check(b, a)

    def test_bare_usage(self):

        b = u"""
        import builtins
        hasattr(builtins, "quit")"""
        a = u"""
        import __builtin__
        hasattr(__builtin__, "quit")"""
        self.check(b, a)
