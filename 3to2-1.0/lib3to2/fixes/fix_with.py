u"""
Fixer for from __future__ import with_statement
"""

from lib2to3 import fixer_base
from ..fixer_util import future_import


class FixWith(fixer_base.BaseFix):

    PATTERN = u"with_stmt"

    def transform(self, node, results):
        future_import(u"with_statement", node)
