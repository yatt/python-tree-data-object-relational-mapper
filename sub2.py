#! /usr/bin/python2.6
# coding: utf-8

import models
import adapter_sqlite3
models.setAdapter(adapter_sqlite3.Sqlite3AdjacencyListModelAdapter())

# 省庁クラス
class Ministry(models.Model):
    cols = [
        ('seq', int),
        ('name', unicode),
        ]
    def __repr__(self):
        return self.name

if __name__ == '__main__':
    Ministry.dump(sortby = lambda n,m: cmp(n.seq, m.seq))
