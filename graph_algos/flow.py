from numpy import inf

class Flow:
    def compute_flow(self, vertices_indexes, u, out_distances, all_distances):
        flow_u = 0
        for v in vertices_indexes:
            if u != v:
                denominator = out_distances[v]
                if denominator != -1:
                    numerator = float(all_distances[v])
                    flow_u += (numerator/denominator)
        B_u = len([d for d in all_distances if d!=inf])
        return (flow_u/B_u)
