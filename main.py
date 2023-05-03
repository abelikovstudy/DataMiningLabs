import matplotlib.pyplot as plt
import pandas as pd

CLUST_N = 2
DIM_N = 4
POINT_N = 150


class Point:
    # x = x1 x2 .. xn
    def __init__(self, x):
        self.x = x
        self.clust = CLUST_N

    def to_clust(self, CC):
        n = CLUST_N
        d = 2**31
        for c in CC:
            if c.dist(self) < d:
                n = c.clust
                d = c.dist(self)
        self.clust = n


class Cluster(Point):
    def __init__(self, cl, x):
        Point.__init__(self, x)
        self.clust = cl
        self.N = 0

    def dist(self, p):
        dd = 0.0
        for i in range(DIM_N):
            dd += (self.x[i] - p.x[i])**2
        return dd

    def eval(self, p_set):
        self.N = 0.02
        for i in range(DIM_N):
            self.x[i] = 0.0
        for p in p_set:
            if p.clust == self.clust:
                self.N += 1
                for i in range(DIM_N):
                    self.x[i] += p.x[i]
        for i in range(DIM_N):
            self.x[i] /= self.N




beer = pd.read_csv("C:\\Users\\user\\Documents\\datamining-git\\beer.csv")
cat_columns = beer.select_dtypes(['bool']).columns
beer[cat_columns] = beer[cat_columns].apply(lambda x: pd.factorize(x)[0])

points_set = [Point([beer["OG"][i], beer["ABV"][i], beer["pH"][i], beer["IBU"][i]]) for i in range(len(beer))]
cluster_set = [Cluster(1, [69.8,10.7,6.6,3.6]), Cluster(0, [85.2,12.3,9.4,5.3])]
colors = ['#0000FF', '#00FF00']

Prec0 = 0.0
Prec = 0
while True:

    for p in points_set:
        p.to_clust(cluster_set)
    for cl in cluster_set:
        cl.eval(points_set)

    fig, axes = plt.subplots(3, 2, figsize=(14, 8))
    n = 0
    for i in range(DIM_N):
        for j in range(i+1, DIM_N):
            ix = int(n/ 3)
            iy = int(n % 3)
            for k in range(POINT_N):
                axes[ix][iy].scatter(points_set[k].x[i], points_set[k].x[j], c = colors[beer["style"][k]], s = 20)
            for c in cluster_set:
                axes[ix][iy].scatter(c.x[i], c.x[j], c = 'red', s = 60, marker='*')

            axes[ix][iy].set_xlabel("$Axis: (" + str(i) + ", " + str(j) + ')$', fontsize = 12)
            axes[ix][iy].set_xticks([])
            axes[ix][iy].set_yticks([])
            n += 1
    fig.tight_layout()
    plt.title(str(Prec))
    plt.show()

    n = 0
    for i in range(len(beer)):
        if points_set[i].clust == beer["style"][i]:
            n += 1
    Prec = float(n)/len(beer)
    print('=====>', Prec)
    if abs(Prec - Prec0) < 0.001:
        break
    Prec0 = Prec