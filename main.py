
import pandas as pd
import matplotlib.pyplot as plt

bills = pd.read_csv("C:\\Users\\user\\Documents\\datamining-git\\mall.csv")
cat_columns = bills.select_dtypes(['bool']).columns
bills[cat_columns] = bills[cat_columns].apply(lambda x: pd.factorize(x)[0])
style = bills['gender'].values

for i in range(0, len(bills)):
    plt.scatter(bills['income'][i], bills['spend'][i], color = (1.0-style[i], 0.0, style[i]), s=20)
plt.show()

KNBR_N = 5

class POINT:
    def __init__(self, x, y, pH,):
        self.x = x
        self.y = y
        self.pH = pH
        self.kn = [0 for i in range(0, KNBR_N)]
        self.clust = 0

    def neighbors(self, A):
        l = [i for i in range(0, len(A))]
        cl = [0,0]
        for k in range(0, KNBR_N):
            i0 = 0
            d0 = 1.0e+99
            cl[A['gender'][i0]] += 1
            for i in l:
                d = (self.x - A['income'][i])**2 + (self.y - A['spend'][i])**2 # 69%
                d += (self.pH - A['Age'][i])**2 

                if d0 > d and d > 0.0:
                    cl[A['gender'][i0]] -= 1
                    i0 = i
                    cl[A['gender'][i0]] += 1
                    d0 = d
            self.kn[k] = i0
            l.remove(i0)
        if cl[0] > cl[1]:
            self.clust = 0
        else:
            self.clust = 1


PP = [POINT(bills['income'][i], bills['spend'][i], bills['Age'][i]) for i in range(0, len(bills))]

for p in PP:
    p.neighbors(bills)
    plt.scatter(p.x, p.y, color=(1.0-float(p.clust), 0.0, float(p.clust)), s=20)
plt.show()

n = 0
for i in range(0, len(bills)):
    if PP[i].clust == bills['gender'][i]:
        n += 1

print('=====>', float(n)/len(bills))