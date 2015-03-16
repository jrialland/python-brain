u"""
Fixer for method.__X__ -> method.im_X
"""

from lib2to3 import fixer_base
from lib2to3.fixer_util import Name

MAP = {
    u"__func__": u"im_func",
    u"__self__": u"im_self"
    # Fortunately, im_self.__class__ == im_class in 2.5.
}


class FixMethodattrs(fixer_base.BaseFix):
    PATTERN = u"""
    power< any+ trailer< '.' attr=('__func__' | '__self__') > any* >
    """

    def transform(self, node, results):
        attr = results[u"attr"][0]
        new = unicode(MAP[attr.value])
        attr.replace(Name(new, prefix=attr.prefix))
