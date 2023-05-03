import matplotlib.pyplot as plt
import random
import math

POINTS_COUNT = 400


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visited = False
        self.cluster = None


class Cluster:
    def __init__(self):
        self.points = []


class DENSITY:
    def __init__(self, eps):
        self.eps = eps
        self.min_pts = 1

    def _eps_neighborhood(self, point_p, point_q):
        return (point_p.x - point_q.x) ** 2 + (point_p.y - point_q.y) ** 2 <= self.eps ** 2

    def _region_query(self, point, points):
        neighbors = []
        for point_q in points:
            if self._eps_neighborhood(point, point_q):
                neighbors.append(point_q)
        return neighbors

    def _expand_cluster(self, point, neighbors, cluster, points):
        cluster.points.append(point)
        point.cluster = cluster
        for point_q in neighbors:
            if not point_q.visited:
                point_q.visited = True
                neighbors_q = self._region_query(point_q, points)
                if len(neighbors_q) >= self.min_pts:
                    neighbors += neighbors_q
            if not point_q.cluster:
                cluster.points.append(point_q)
                point_q.cluster = cluster

    def fit(self, points):
        clusters = []
        for point in points:
            if point.visited:
                continue
            point.visited = True
            neighbors = self._region_query(point, points)
            if len(neighbors) < self.min_pts:
                point.cluster = None
            else:
                cluster = Cluster()
                clusters.append(cluster)
                self._expand_cluster(point, neighbors, cluster, points)
        return clusters


def gen_data_clouds(points, count_points):
    for i in range(0, count_points):
        if random.random() < 0.5:
            points[i].x = random.normalvariate(-1.0, 0.4)
            points[i].y = random.normalvariate(-1.0, 0.3)
        else:
            points[i].x = random.normalvariate(1.0, 0.3)
            points[i].y = random.normalvariate(0.5, 0.4)
    return


def gen_data_cloud(points, count_points):
    for i in range(0, count_points):
        if random.random() < 0.5:
            points[i].x = random.normalvariate(-0.3, 0.5)
            points[i].y = random.normalvariate(-0.5, 0.5)
        else:
            points[i].x = random.normalvariate(0.3, 0.5)
            points[i].y = random.normalvariate(0.5, 0.5)
    return


def gen_data_moons(points, count_points):
    for i in range(0, count_points):
        deg = 3.14 * random.random()
        r = 0.2 * random.normalvariate(0.0, 0.4) + 1.5
        if random.random() < 0.5:
            points[i].x = 0.5 + r * math.cos(deg)
            points[i].y = -0.25 + r * math.sin(deg)
        else:
            points[i].x = -0.5 + r * math.cos(deg)
            points[i].y = 0.25 - r * math.sin(deg)
    return


def gen_data_circle(points, count_points):
    for i in range(0, count_points):
        deg = 3.14 * random.random()
        r = 0.2 * random.normalvariate(0.0, 0.4) + 0.9
        if random.random() < 0.5:
            points[i].x = 0.5 + r * math.cos(deg)
            points[i].y = 0.25 + r * math.sin(deg)
        else:
            points[i].x = 0.5 + r * math.cos(deg)
            points[i].y = 0.25 - r * math.sin(deg)
    return


def draw_clusters(clusters, plotName, axis):
    COLORS = ['green', 'blue', 'red', 'yellow', 'violet', 'aqua', 'plum', 'wheat']
    for i, cluster in enumerate(clusters):
        for point in cluster.points:
            color = 'black'
            if len(COLORS) > i:
                color = COLORS[i]
            axis.scatter(point.x, point.y, c=color, marker='.')
    axis.set_xlabel(plotName)


if __name__ == "__main__":
    POINTS1 = [Point(0.0, 0.0) for _ in range(0, POINTS_COUNT)]
    POINTS2 = [Point(0.0, 0.0) for _ in range(0, POINTS_COUNT)]
    POINTS3 = [Point(0.0, 0.0) for _ in range(0, POINTS_COUNT)]
    POINTS4 = [Point(0.0, 0.0) for _ in range(0, POINTS_COUNT)]
    density1 = DENSITY(eps=1.5)
    density2 = DENSITY(eps=0.5)
    density3 = DENSITY(eps=0.25)
    density4 = DENSITY(eps=0.25)

    f = plt.figure()
    f, axes = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True)

    gen_data_cloud(POINTS1, POINTS_COUNT)
    CLUSTERS1 = density1.fit(POINTS1)
    draw_clusters(CLUSTERS1, "Облако", axes[0][0])

    gen_data_clouds(POINTS2, POINTS_COUNT)
    CLUSTERS2 = density2.fit(POINTS2)
    draw_clusters(CLUSTERS2, "Два облака", axes[0][1])

    gen_data_moons(POINTS3, POINTS_COUNT)
    CLUSTERS3 = density3.fit(POINTS3)
    draw_clusters(CLUSTERS3, "Луны", axes[1][0])

    gen_data_circle(POINTS4, POINTS_COUNT)
    CLUSTERS4 = density4.fit(POINTS4)
    draw_clusters(CLUSTERS4, "Круг", axes[1][1])

    plt.show()