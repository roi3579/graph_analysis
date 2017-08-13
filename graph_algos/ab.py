from numpy import inf

class Ab:
    def compute_ab(self, vertices_indexes, attractor_basin_out_dist, attractor_basin_in_dist):
        avg_out=self.calc_avg_for_dist(len(vertices_indexes),attractor_basin_out_dist)
        avg_in =self.calc_avg_for_dist(len(vertices_indexes),attractor_basin_in_dist)
        attractor_basin_details=[attractor_basin_out_dist,avg_out,attractor_basin_in_dist, avg_in]
        return self.calc_final_attraction_basin(attractor_basin_details,vertices_indexes)

    def calc_final_attraction_basin(self, attractor_basin_details, vertices_indexes):
        attractor_basin = {}
        avg_out=attractor_basin_details[1]
        avg_in = attractor_basin_details[3]
        for index in vertices_indexes:
            alpha = 2
            out_dist = attractor_basin_details[0][index]
            in_dist = attractor_basin_details[2][index]
            numerator = 0
            denominator = 0
            for m in range(1,len(in_dist)):
                numerator = numerator + (in_dist[m] / avg_in[m]) * alpha ** (-m)
            for k in range(1,len(out_dist)):
                denominator = denominator + (out_dist[k] / avg_out[k]) * alpha ** (-k)
            if (denominator == 0):
                attractor_basin[index] = -1
            else:
                attractor_basin[index] = numerator / denominator
        return attractor_basin

    def calc_avg_for_dist(self, num_of_nodes_in_gragh,count_dist):
        all_dist_count={}
        avg_for_dist={}
        for i in range (0,len(count_dist)):
            for j in range(1,len(count_dist[i])):
                if (j not in all_dist_count.keys()):
                    all_dist_count[j]=count_dist[i][j]
                else:
                    all_dist_count[j]+=count_dist[i][j]
        for l in all_dist_count.keys():
            avg=float(all_dist_count[l])/num_of_nodes_in_gragh
            avg_for_dist[l]=avg
        return avg_for_dist




