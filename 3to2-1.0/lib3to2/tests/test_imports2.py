from test_all_fixers import lib3to2FixerTestCase


class Test_imports2(lib3to2FixerTestCase):
    fixer = u"imports2"

    def test_name_usage_simple(self):

        b = u"""
        import urllib.request
        urllib.request.urlopen(spam)"""

        a = u"""
        import urllib2, urllib
        urllib2.urlopen(spam)"""

        self.check(b, a)

        b = u"""
        if True:
            import http.server
        else:
            import this
        while True:
            http.server.HTTPServer(('localhost', 80), http.server.SimpleHTTPRequestHandler)
        else:
            import urllib.request"""
        a = u"""
        if True:
            import CGIHTTPServer, SimpleHTTPServer, BaseHTTPServer
        else:
            import this
        while True:
            BaseHTTPServer.HTTPServer(('localhost', 80), SimpleHTTPServer.SimpleHTTPRequestHandler)
        else:
            import urllib2, urllib"""
        self.check(b, a)

    def test_name_scope_def(self):

        b = u"""
        import urllib.request
        def importing_stuff():
            import urllib.request
            urllib.request.urlopen(stuff)
        urllib.request.urlretrieve(stuff)"""
        a = u"""
        import urllib2, urllib
        def importing_stuff():
            import urllib2, urllib
            urllib2.urlopen(stuff)
        urllib.urlretrieve(stuff)"""
        self.check(b, a)

        b = u"""
        import math, urllib.request, http.server, dbm

        w = dbm.whichdb()
        g = dbm.gnu()
        a = dbm.open()"""
        a = u"""
        import math
        import anydbm, whichdb, dbm
        import CGIHTTPServer, SimpleHTTPServer, BaseHTTPServer
        import urllib2, urllib

        w = whichdb.whichdb()
        g = dbm.gnu()
        a = anydbm.open()"""
        self.check(b, a)

    def test_name_scope_if(self):

        b = u"""
        if thing:
            import http.server
        elif other_thing:
            import xmlrpc.server
        if related_thing:
            myServ = http.server.HTTPServer(('localhost', '80'), http.server.CGIHTTPRequestHandler)
        elif other_related_thing:
            myServ = xmlrpc.server.SimpleXMLRPCServer(('localhost', '80'), CGIXMLRPCRequestHandler)

        # just for kicks...
        monkey_wrench_in_the_works = http.server.SimpleHTTPRequestHandler"""

        a = u"""
        if thing:
            import CGIHTTPServer, SimpleHTTPServer, BaseHTTPServer
        elif other_thing:
            import DocXMLRPCServer, SimpleXMLRPCServer
        if related_thing:
            myServ = BaseHTTPServer.HTTPServer(('localhost', '80'), CGIHTTPServer.CGIHTTPRequestHandler)
        elif other_related_thing:
            myServ = SimpleXMLRPCServer.SimpleXMLRPCServer(('localhost', '80'), CGIXMLRPCRequestHandler)

        # just for kicks...
        monkey_wrench_in_the_works = SimpleHTTPServer.SimpleHTTPRequestHandler"""
        self.check(b, a)

    def test_name_scope_try_except(self):

        b = u"""
        try:
            import http.server
        except ImportError:
            import xmlrpc.server

        # some time has passed, and we know that http.server was bad.
        srv = xmlrpc.server.DocXMLRPCServer(addr, xmlrpc.server.DocCGIXMLRPCRequestHandler)

        # some more time has passed, and we know that http.server is good.
        srv = http.server.HTTPServer(addr, http.server.CGIHTTPRequestHandler)"""

        a = u"""
        try:
            import CGIHTTPServer, SimpleHTTPServer, BaseHTTPServer
        except ImportError:
            import DocXMLRPCServer, SimpleXMLRPCServer

        # some time has passed, and we know that http.server was bad.
        srv = DocXMLRPCServer.DocXMLRPCServer(addr, DocXMLRPCServer.DocCGIXMLRPCRequestHandler)

        # some more time has passed, and we know that http.server is good.
        srv = BaseHTTPServer.HTTPServer(addr, CGIHTTPServer.CGIHTTPRequestHandler)"""
        self.check(b, a)

    def test_name_multiple_imports(self):

        b = u"""
        import math, http.server, urllib.request, string"""
        a = u"""
        import math, string
        import urllib2, urllib
        import CGIHTTPServer, SimpleHTTPServer, BaseHTTPServer"""

        self.check(b, a)

    def test_name_mutiple_imports_indented(self):

        b = u"""
        def indented():
            import math, http.server, urllib.request, string"""
        a = u"""
        def indented():
            import math, string
            import urllib2, urllib
            import CGIHTTPServer, SimpleHTTPServer, BaseHTTPServer"""

        self.check(b, a)

    def test_from_single(self):

        b = u"from urllib.request import urlopen"
        a = u"from urllib2 import urlopen"
        self.check(b, a)

        b = u"from urllib.request import urlopen\n"\
            u"from urllib.parse import urlencode"
        a = u"from urllib2 import urlopen\n"\
            u"from urllib import urlencode"
        self.check(b, a)

        b = u"from tkinter.simpledialog import SimpleDialog"
        a = u"from SimpleDialog import SimpleDialog"
        self.check(b, a)

    def test_from_star(self):

        b = u"""
        def try_import(package):
            try:
                from http.server import *
                print('success')
            except ImportError:
                print('failure', end="")
                print('try again!')
        """
        a = u"""
        def try_import(package):
            try:
                from BaseHTTPServer import *
                from CGIHTTPServer import *
                from SimpleHTTPServer import *
                print('success')
            except ImportError:
                print('failure', end="")
                print('try again!')
        """
        self.check(b, a, ignore_warnings=True)

        b = u"""
        def testing_http_server():
            from http.server import *
            test_all_imports()
        def testing_xmlrpc_server():
            from xmlrpc.server import *
            test_all_imports()
        """
        a = u"""
        def testing_http_server():
            from BaseHTTPServer import *
            from CGIHTTPServer import *
            from SimpleHTTPServer import *
            test_all_imports()
        def testing_xmlrpc_server():
            from SimpleXMLRPCServer import *
            from DocXMLRPCServer import *
            test_all_imports()
        """
        self.check(b, a, ignore_warnings=True)

    def test_from_list(self):

        b = u"""
        with open('myFile', 'r') as myFile:
            from urllib.request import install_opener, urlretrieve, unquote as billybob
            fileList = [ln for ln in myFile]"""
        a = u"""
        with open('myFile', 'r') as myFile:
            from urllib import urlretrieve, unquote as billybob
            from urllib2 import install_opener
            fileList = [ln for ln in myFile]"""
        self.check(b, a, ignore_warnings=True)

    if False:
        def test_modulefrom(self):

            b = u"""
            if spam.is_good():
                from urllib import request, parse
                request.urlopen(spam_site)
                parse.urlencode(spam_site)"""
            a = u"""
            if spam.is_good():
                import urllib
                import urllib2
                urllib2.urlopen(spam_site)
                urllib.urlencode(spam_site)"""
            self.check(b, a)
