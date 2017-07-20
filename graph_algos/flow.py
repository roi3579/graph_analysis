from numpy import inf

class Flow:
    def compute_flow(self, g, vertices_list, threshold):
        if vertices_list is None:
            vertices_list = range(g.vcount())
        max_B_v =0
        B_u ={}
        for u in vertices_list:
            B_u[u]= len(set(g.bfs(vid=4, mode="ALL")[0]))
            max_B_v = max(max_B_v,B_u[u])
        max_B_v = float(max_B_v)
        flow_dict = {}
        for u in vertices_list:
            flow_u = 0
            if B_u[u]/max_B_v > threshold:
                for v in vertices_list:
                    if u != v:
                        denominator = g.shortest_paths(source=u, target=v, mode="OUT")[0][0]
                        if denominator != inf:
                            numerator = float(g.shortest_paths(source=u, target=v, mode="ALL")[0][0])
                            flow_u += (numerator/denominator)
            flow_dict[u] = flow_u

        return flow_dict




