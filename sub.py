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
        #return '<Ministry %s id=%s>' % (self.name, self.id)
        return '%s' % self.name
    def __cmp__(n, m):
        return cmp(n.seq, m.seq)
        

def it():
    Ministry.sync()
    m = Ministry(name = 'pyramid')
    n = Ministry(name = 'Django')
    m.update()
    n.hook(m)
    n.update()
    print m.children()

def jt():
    Ministry.sync()
    root = Ministry(name = 'root')
    root.update()
    for i in range(100):
        n = Ministry(name = 'mini%02d' % i)
        n.hook(root)
        n.update()
        root = n
    Ministry.lookup(1).delete()    

def kt():
    Ministry.sync()
    fromdict(dat)
    Ministry.dump(sortby = cmp)

def main():
    #kt()
    Ministry.dump(sortby = cmp)

def fromdict(dic):
    lst = []
    for key in dic:
        seq,name = key
        m = Ministry(name = name, seq = seq)
        m.update()
        if dic[key] is not None:
            ns = fromdict(dic[key])
            for n in ns:
                n.hook(m)
                #print 'bind',n,'->',m
                n.update()
        lst.append(m)
    return lst

dat = {
    (0, u'内閣'): {
        (0, u'内閣官房'): None,
        (1, u'内閣法制局'): None,
        (2, u'安全保障会議'): None,
        (3, u'人事院'): None,
        (4, u'内閣府'): {
            (0, u'北方対策本部'): None,
            (1, u'金融危機対応会議'): None,
            (2, u'食育推進会議'): None,
            (3, u'少子化社会対策会議'): None,
            (4, u'高齢社会対策会議'): None,
            (5, u'中央交通安全対策会議'): None,
            (6, u'犯罪被害者等施策推進会議'): None,
            (7, u'自殺総合対策会議'): None,
            (8, u'消費者政策会議'): None,
            (9, u'国際平和協力本部'): None,
            (10, u'日本学術会議'): None,
            (11, u'官民人材交流センター'): None,
            (12, u'宮内庁'): None,
            (13, u'公正取引委員会'): None,
            (14, u'国家公安委員会'): {
                (0, u'警察庁'): None
            },
            (0, u'金融庁'): None,
            (1, u'消費者庁'): None,
        },
        (5, u'総務省'): {
            (0, u'中央選挙管理会'): None,
            (1, u'政治資金適正化委員会'): None,
            (2, u'公害等調整委員会'): None,
            (3, u'消防庁'): None,
        },
        (6, u'総務省'): {
            (0, u'検察庁'): None,
            (0, u'公安審査委員会'): None,
            (0, u'公安調査庁'): None,
        },
        (7, u'外務省'): {
            (0, u'在外公館'): None,
        },
        (8, u'財務省'): {
            (0, u'国税庁'): {
                (0, u'国税不服審判所'): None,
            },
        },
        (9, u'文部科学省'): {
            (0, u'日本学士院'): None,
            (1, u'地震調査研究推進本部'): None,
            (2, u'日本ユネスコ国内委員会'): None,
            (3, u'文化庁'): {
                (0, u'日本芸術院'): None,
            },
        },
        (10, u'厚生労働省'): {
            (0, u'中央労働委員会'): None,
        },
        (11, u'農林水産省'): {
            (0, u'農林水産技術会議'): None,
            (1, u'林野庁'): None,
            (2, u'水産庁'): {
                (0, u'太平洋広域漁業調整委員会'): None,
                (1, u'日本海・九州西広域漁業調整委員会'): None,
                (2, u'瀬戸内海広域漁業調整委員会'): None,
            },
        },
        (12, u'経済産業省'): {
            (0, u'資源エネルギー庁'): {
                (0, u'原子力安全・保安院'): None,
            },
            (0, u'特許庁'): None,
            (0, u'中小企業庁'): None,
        },
        (13, u'国土交通省'): {
            (0, u'国土地理院'): None,
            (1, u'小笠原総合事務所'): None,
            (2, u'海難審判所'): None,
            (3, u'観光庁'): None,
            (4, u'気象庁'): None,
            (5, u'運輸安全委員会'): None,
            (6, u'海上保安庁'): None,
        },
        (14, u'環境省'): {
            (0, u'公害対策会議'): None,
        },
        (15, u'防衛省'): {
            (0, u'統合幕僚監部'): None,
            (1, u'陸上幕僚監部'): None,
            (2, u'海上幕僚監部'): None,
            (3, u'航空幕僚監部'): None,
            (4, u'陸上自衛隊'): None,
            (5, u'海上自衛隊'): None,
            (6, u'航空自衛隊'): None,
            (7, u'情報本部'): None,
            (8, u'技術研究本部'): None,
            (9, u'装備施設本部'): None,
            (10, u'防衛監察本部'): None,
            (11, u'外国軍用品審判所'): None,
        },
    },
    (1, u'会計監査院'): None,
}

if __name__ == '__main__':
    main()
