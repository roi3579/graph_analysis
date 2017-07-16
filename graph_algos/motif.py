import itertools


class Motif:

    def __init__(self, directed, veriation_folder):
        self._motif_3_veriation_dict = self.__init_motif_dict(directed, veriation_folder, 3)
        self._motif_4_veriation_dict = self.__init_motif_dict(directed, veriation_folder, 4)
        self._motif_hist = {}

    def __init_motif_dict(self, is_directed, motifs_veriation_folder, motif_number):
        if motif_number == 3:
            bit_format = '06b'
            motif_edges_index = [[0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1]]
        elif motif_number == 4:
            bit_format = '012b'
            motif_edges_index = [[0, 1], [0, 2], [0, 3], [1, 0], [1, 2], [1, 3], [2, 0], [2, 1], [2, 3], [3, 0], [3, 1],
                                 [3, 2]]

        if (is_directed):
            f = open(motifs_veriation_folder + '/' + str(motif_number) + r'_nodes_data_directed_key.txt')
        else:
            f = open(motifs_veriation_folder + '/' + str(motif_number) + r'_nodes_data_undirected_key.txt')

        motifs_edges_dict = {}
        raws = f.readlines()
        motifs_vertices_dict = {}
        for r in raws:
            new_raw = r.replace('\r\n', '')
            clean_raw = new_raw.replace('\t', ',')
            s = clean_raw.split(',')
            if (s[0] == '-1'):
                break;
            if (is_directed):
                bit_string = format((int(s[1])), bit_format)
                motifs_vertices_dict[bit_string] = int(s[0])
                motif_edges = []
                index = 0
                for b in bit_string:
                    if b == '1':
                        motif_edges.append(motif_edges_index[index])
                    index += 1
                motifs_edges_dict[bit_string] = motif_edges
            else:
                motifs_vertices_dict[format((int(s[1])), '03b')] = int(s[0])
        motifs_dict = {}
        motifs_dict['v'] = motifs_vertices_dict
        motifs_dict['e'] = motifs_edges_dict
        return motifs_vertices_dict

    def __neighbor(self,g, vertex):
        return set(g.neighbors(vertex, mode="in")).union(
            set(g.neighbors(vertex, mode="out")))


    def __add_to_hist_by_subgraph(self,subg, comb):
        n=comb[0]
        self._motif_hist[n][self._motif_3_veriation_dict[subg]] += 1

    def __combination_calc(self, g, comb):
        subg = self.__to_subgrap_str(g, comb)
        self.__add_to_hist_by_subgraph(subg, comb)


    def __to_subgrap_str(self,g, comb):
        if (g.is_directed()):
            subg = self.__directed_sub_graph(g, comb)
        else:
            subg = self.__undirected_sub_graph(g, comb)
        return subg


    def __undirected_sub_graph(self,g, comb):
        subg = ''
        for (a, b) in itertools.combinations(comb, 2):
            if (g.are_connected(a, b)):
                subg = subg + '1'
            else:
                subg = subg + '0'
        return subg


    def __directed_sub_graph(self,g, comb):
        subg = ''
        for (a, b) in itertools.permutations(comb, 2):
            if (g.are_connected(a, b)):
                subg = subg + '1'
            else:
                subg = subg + '0'
        return subg


    def __get_sub_tree(self,g, root, veriation, visited_vertices, visited_index):
        if (veriation == (1, 1)):
            neighbors = self.__neighbor(g, root)
            for n in neighbors:
                visited_vertices[n] = visited_index
                visited_index += 1
            for n in neighbors:
                last_neighbors = self.__neighbor(g, n)
                for l in last_neighbors:
                    if (visited_vertices.has_key(l)):
                        if (visited_vertices[root] < visited_vertices[n] < visited_vertices[l]):
                            s = [root, n, l]
                            self.__combination_calc(g, s)
                    else:
                        visited_vertices[l] = visited_index
                        visited_index += 1
                        s = [root, n, l]
                        self.__combination_calc(g, s)
            return [visited_vertices, visited_index]

        if (veriation == (2, 0)):
            neighbors = self.__neighbor(g, root)
            for comb in itertools.combinations(neighbors, 2):
                if (visited_vertices[root] < visited_vertices[comb[0]] < visited_vertices[comb[1]]):
                    if (not (g.are_connected(comb[0],comb[1]) or g.are_connected(comb[1],comb[0]))):
                        s = [root, comb[0], comb[1]]
                        self.__combination_calc(g, s)

    def compute_motif(self,g, vertices_list=None, motif_size=3):
        if vertices_list is None:
            vertices_list = range(g.vcount())

        for v in vertices_list:
            self._motif_hist[v] = [0]*(max(self._motif_3_veriation_dict.values())+1)

        for v in vertices_list:
            visited_vertices = {v: 0}
            [visited_vertices, visited_index] = self.__get_sub_tree(g, v, (1, 1), visited_vertices, 1)
            self.__get_sub_tree(g, v, (2, 0), visited_vertices, visited_index)

        return self._motif_hist

