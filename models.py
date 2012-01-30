#! /usr/bin/python2.6
# coding: utf-8

_adapter =None
def setAdapter(adapter):
    global _adapter
    _adapter = adapter


class Node(object):
    cols = []
    dbtype = {}
    def __init__(self, *args, **kwargs):
        self.prop = kwargs
        self.children = None
        self.parent = None
    def __getattr__(self, name):
        return self.prop.get(name, None)
    def setAttribute(self, key, value):
        self.prop[key] = value
    def getAttribute(self, key):
        return self.prop.get[key]
    @classmethod
    def sync(cls):
        return _adapter.sync(cls)
    @classmethod
    def lookup(cls, id):
        return _adapter.lookup(cls, id)
    def getChildren(self):
        return _adapter.getChildren(self)
    def getParent(self, child):
        return _adapter.getParent(child)
    def sibling(self):
        return _adapter.sibling(self)
    def update(self):
        return _adapter.update(self)
    def append(self, node):
        return _adapter.append(self, node)
    def delete(self):
        return _adapter.delete(self)
    def hook(self, parent):
        return _adapter.hook(self, parent)
    @classmethod
    def find(cls, **kwargs):
        return _adapter.find(cls, **kwargs)
    @classmethod
    def dump(cls, lst = None, depth = 0, sortby = None):
        lst = cls.find(parent_id = -1) if lst is None else lst
        if sortby is not None:
            lst.sort(cmp = sortby)
        for n in lst:
            print '%s%s' % ("    " * depth, repr(n))
            cls.dump(n.getChildren(), depth  + 1, sortby)

Model = Node
