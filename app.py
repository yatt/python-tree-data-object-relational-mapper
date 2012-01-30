import models
import adapter_sqlite3

models.setAdapter(adapter_sqlite3.Sqlite3AdjacencyListModelAdapter())

# クリティカルパスの計算
#  最適化問題を解く
# 3Dボーンモデル
# 3Dシーングラフ
# ニューラルネットワーク
# 決定木
class DicisionTreeNode(models.Model):
    cols = [
        ('', ),
        ('', ),
        ('', ),
        ]


def buildDicisionTree():
    conn = sqlite3.conect('target.sqlite')
    for row in conn.execute('select * from table'):
        DicisionTreeNode


def main():
    buildDicisionTree()


if __name__ == '__main__':
    main()
