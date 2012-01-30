#! /usr/bin/python2.6
# coding: utf-8

import sqlite3

def c(obj):
    if type(obj) is type:
        return obj.__name__
    else:
        return obj.__class__.__name__

def q(stmt):
    #print 'sql:',stmt
    conn = sqlite3.connect('table.sqlite')
    curs = conn.cursor()
    lst = curs.execute(stmt).fetchall()
    rowid = curs.lastrowid
    conn.commit()
    conn.close()
    if stmt.split()[0].lower() == 'select':
        return lst
    elif stmt.split()[0].lower() == 'insert':
        return rowid


class Sqlite3BaseAdapter(object):
    iso = 'EXCLUSIVE'
    dbtype = {
        int   : 'integer',
        float : 'real',
        str   : 'text',
        unicode: 'text',
    }
    hidden = []
    def sync(self, cls):
        fs = []
        for n,t in self.hidden + cls.cols:
            fs.append('%s %s' % (n, self.dbtype[t]))
        fs = ', '.join(fs)
        
        args = (cls.__name__, self.dbtype[int], fs)
        q('drop table if exists ' + c(cls))
        q('create table %s (id %s primary key, %s)' % args)

    def colcsv(self, cls):
        return ','.join(name for name,_ in self.hidden + cls.cols)



class Sqlite3AdjacencyListModelAdapter(Sqlite3BaseAdapter):
    hidden = [('parent_id', int)]
    def __init__(self):
        super(Sqlite3AdjacencyListModelAdapter, self).__init__()
    
    def factory(self, cls, row):
        name = map(lambda n:n[0], self.hidden + cls.cols)
        kwargs = dict(zip(name, row[1:]))
        obj = cls(**kwargs)
        obj.id = row[0]
        return obj

    def getChildren(self, parent):
        cls = parent.__class__
        name = map(lambda n:n[0], self.hidden + cls.cols)
        lst = []
        fn = lambda row: self.factory(cls, row)
        return map(fn, q('select * from %s where parent_id = %d' % (c(cls), parent.id)))
    
    def getParent(self, node):
        return lookup(node.parent_id)
 
    def update(self, node):
        # upsert
        cls = node.__class__
        name = c(cls)
        stmt = ''
        if node.parent_id is None:
            node.parent_id = -1
        #print 'register as ', node.parent_id
        if node.id is None:
            newid = 'select coalesce(max(id), 0) + 1 from %s' % name
            args = [name, newid] + [','.join("'%s'" % getattr(node, name) for name,_ in self.hidden + cls.cols)]
            stmt = 'insert into %s values ((%s), %s)' % tuple(args)
            node.id = q(stmt)
        else:
            fs = ','.join("%s = '%s'" % (name, getattr(node, name)) for name,_ in self.hidden + cls.cols)
            args = (name, fs, node.id)
            stmt = 'update %s set %s where id = %d' % args
            q(stmt)

    # 隣接リストだと子側が親IDをもつのでparent.append(child)よりchild.hook(parent)とした方がoop的に良さそう
    def hook(self, child, parent):
        child.parent_id = parent.id

    def delete(self, subnode):
        self.traverse(subnode, lambda i: q('delete from %s where id = %d' % (c(subnode), i)))
    
    def traverse(self, subnode, callback):
        stk = [subnode.id]
        while len(stk) > 0:
            nodeid = stk.pop()
            rows = q('select * from %s where parent_id = %d' % (c(subnode), nodeid))
            for row in rows:
                stk.append(row[0])
            callback(nodeid)
    
    def lookup(self, cls, id):
        name = self.colcsv(cls)
        row = q('select * from %s where id = %d' % (c(cls), id))
        return self.factory(cls, row[0]) if len(row) > 0 else None
    
    def find(self, cls, **kwargs):
        cond = ' AND '.join("%s = '%s'" % (key, kwargs[key]) for key in kwargs)
        lst = q('select * from %s where %s' % (c(cls), cond))
        fn = self.factory
        return map(lambda row:fn(cls, row), lst)
    

class NestedSetModelAdapter(object):
    # ref: http://gihyo.jp/dev/serial/01/sql_academy2/000601
    hidden = [('lft', int), ('rgt', int)]

class PathEnumerationModelAdapter(object):
    hidden = [('path', str)]
