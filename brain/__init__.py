# -*- coding : utf-8 -*-

"""
A lightweight pure-python neural network library.
"""
__author__ = "Julien Rialland"
__copyright__ = "Copyright 2015, J.Rialland"
__license__ = "Apache License 2.0"
__version__ = "0.4.2"
__maintainer__ = __author__
__email__ = "julien.rialland@gmail.com"
__status__ = "Production"

import sys

pyversion = sys.version_info[0]

if pyversion > 2:
    import brain.brain_py3
    impl_module = brain.brain_py3
else:
    import brain.brain_py2
    impl_module = brain.brain_py2

__all__ = []
for sym in dir(impl_module):
    if not sym.startswith('_'):
        __all__.append(sym)
        globals()[sym] = getattr(impl_module, sym)
