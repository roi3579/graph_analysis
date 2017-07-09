import numpy as np
from numpy import inf



class BFS:
    def bfs_momemts(self,graph,vertices_indexes=None):
        if vertices_indexes is None:
            vertices_indexes = range(len(graph.vs))
        bfs_dist = self.__calc_bfs_dist(graph, vertices_indexes)
        dist_moments = {}
        for key in bfs_dist.keys():
            lst = []
            lst.append(float(np.average(bfs_dist[key], weights=range(1,len(bfs_dist[key])+1))))
            lst.append(float(np.std(bfs_dist[key])))
            dist_moments[key] = lst
        return dist_moments

    def __calc_bfs_dist(self, graph, vertices_indexes):
        bfs_dist = {}
        for v in vertices_indexes:
            distances = graph.shortest_paths_dijkstra(source=[v])[0]
            distances = [d if d!=inf else -1 for d in distances]
            vertex_distance_distribution = np.zeros(max(distances)+1)
            for distance in distances:
                if distance != -1:
                    vertex_distance_distribution[distance]+=1
            bfs_dist[v] = vertex_distance_distribution
        return bfs_dist
