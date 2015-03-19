#/usr/bin env python
# -*- coding:utf-8 -*-

import sys
import os.path
import glob
import unittest

suite = unittest.TestSuite()
test_modules = [os.path.basename(str[0:len(
    str) - 3]) for str in glob.glob(os.path.join(os.path.dirname(__file__), 'test_*.py'))]
for module in test_modules:
    try:
        # If the module defines a suite() function, call it to get the suite.
        mod = __import__(module, globals(), locals(), ['suite'])
        suitefn = getattr(mod, 'suite')
        suite.addTest(suitefn())
    except (ImportError, AttributeError):
        # else, just load all the test cases from the module.
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(module))

if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    if len(result.errors) + len(result.failures) == 0:
        sys.exit(0)
    else:
        sys.exit(1)
