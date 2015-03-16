u"""
Fixer for input(s) -> raw_input(s).
"""

from lib2to3 import fixer_base
from lib2to3.fixer_util import Name


class FixInput(fixer_base.BaseFix):

    PATTERN = u"""
              power< name='input' trailer< '(' [any] ')' > any* >
              """

    def transform(self, node, results):
        name = results[u"name"]
        name.replace(Name(u"raw_input", prefix=name.prefix))
