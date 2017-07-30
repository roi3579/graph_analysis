import numpy as np
from numpy import inf
from flow import Flow
from ab import Ab

class BFS:
    def __init__(self):
        self._flow = Flow()
        self._ab = Ab()

    def bfs(self,graph,vertices_indexes=None):
        if vertices_indexes is None:
            vertices_indexes = range(len(graph.vs))

        flow_dict = {}
        bfs_dist = {}
        attractor_basin_out_dist=[]
        attractor_basin_in_dist=[]
        # max_B_v =0
        # B_u ={}
        # for u in vertices_indexes:
        #     B_u[u]= len(set(graph.bfs(vid=4, mode="ALL")[0]))
        #     max_B_v = max(max_B_v,B_u[u])
        # max_B_v = float(max_B_v)

        for u in vertices_indexes:
            out_distances = graph.shortest_paths_dijkstra(source=[u])[0]
            all_distances = graph.shortest_paths_dijkstra(source=[u], mode="ALL")[0]
            in_distances = graph.shortest_paths_dijkstra(source=[u], mode="IN")[0]

            out_distances = [d if d!=inf else -1 for d in out_distances]
            vertex_distance_distribution = np.zeros(max(out_distances)+1)
            for distance in out_distances:
                if distance != -1:
                    vertex_distance_distribution[distance]+=1

            in_distances = [d if d!=inf else -1 for d in in_distances]
            vertex_in_distance_distribution = np.zeros(max(in_distances)+1)
            for distance in in_distances:
                if distance != -1:
                    vertex_in_distance_distribution[distance]+=1

            flow_dict[u] = self._flow.compute_flow(vertices_indexes, u, out_distances, all_distances)

            attractor_basin_out_dist.append(vertex_distance_distribution.tolist())
            attractor_basin_in_dist.append(vertex_in_distance_distribution.tolist())

            bfs_dist[u] = vertex_distance_distribution

        dist_moments = self.bfs_momemts(bfs_dist)

        attractor_basin = self._ab.compute_ab(vertices_indexes, attractor_basin_out_dist, attractor_basin_in_dist)

        return dist_moments, flow_dict, attractor_basin

    def bfs_momemts(self, bfs_dist):
        dist_moments = {}

        for key in bfs_dist.keys():
            lst = []
            lst.append(float(np.average(bfs_dist[key], weights=range(1,len(bfs_dist[key])+1))))
            lst.append(float(np.std(bfs_dist[key])))
            dist_moments[key] = lst
