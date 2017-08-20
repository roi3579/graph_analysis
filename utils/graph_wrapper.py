from igraph import Graph
from graph_algos.motif import Motif
from graph_algos.flow import Flow
from graph_algos.propagation_features import Propagation
import pymysql
from graph_algos.bfs import BFS
import random
import json


class GraphWrapper:
    def __init__(self):
        self._graph = None
        self._vertex_to_index_dict = {}
        self._index_to_vertex_dict = {}
        self._number_of_vertices = 0
        self._bfs = BFS()
        self._flow = Flow()
        self._propagation = Propagation()

    def __init__edges_list_from_list(self, edge_list):
        edge_to_weight_dict = {}
        for edge in edge_list:
            v_src = edge[0]
            v_trg = edge[1]
            weight = 1.0
            self.__add_new_vertex(v_src)
            self.__add_new_vertex(v_trg)
            src_index = self._vertex_to_index_dict[v_src]
            trg_index = self._vertex_to_index_dict[v_trg]
            edge_to_weight_dict[(src_index, trg_index)] = weight

        return edge_to_weight_dict

    def __init_edges_list_from_file(self, file_path):
        edge_to_weight_dict = {}
        lines = open(file_path).readlines()
        for line in lines:
            words = line.replace('\n', '').replace('\r', '').replace('\t', ' ').split(' ')
            v_src = words[0]
            v_trg = words[1]
            weight = float(words[2])
            self.__add_new_vertex(v_src)
            self.__add_new_vertex(v_trg)
            src_index = self._vertex_to_index_dict[v_src]
            trg_index = self._vertex_to_index_dict[v_trg]
            edge_to_weight_dict[(src_index, trg_index)] = weight

        return edge_to_weight_dict

    def __init_edges_list_from_db(self, file_path):
        edge_to_weight_dict = {}
        with open(file_path, 'r') as f:
            db_paras = json.load(f)
        connection_params = db_paras['connection_details']
        cnx = pymysql.connect(user=connection_params['user'],
                              password=connection_params['pass'],
                              host=connection_params['host'],
                              database=connection_params['database'])

        cursor = cnx.cursor()

        query = db_paras['edges_query']
        cursor.execute(query)
        count = 0
        for v_src, v_trg in cursor:
            count += 1
            v_src = str(v_src)
            v_trg = str(v_trg)
            self.__add_new_vertex(v_src)
            self.__add_new_vertex(v_trg)
            src_index = self._vertex_to_index_dict[v_src]
            trg_index = self._vertex_to_index_dict[v_trg]
            edge_to_weight_dict[(src_index, trg_index)] = 1

        print count
        cnx.close()

        return edge_to_weight_dict

    def __add_new_vertex(self, vertex_name):
        if vertex_name not in self._vertex_to_index_dict:
            self._vertex_to_index_dict[vertex_name] = self._number_of_vertices
            self._index_to_vertex_dict[self._number_of_vertices] = vertex_name
            self._number_of_vertices += 1

    def __init_graph_by_edges_dict(self, edge_to_weight_dict, is_directed):
        self._graph = Graph(directed=is_directed)
        self._graph.add_vertices(self._number_of_vertices)
        self._graph.add_edges(edge_to_weight_dict.keys())
        self._graph.es["weight"] = 1.0
        for edge in edge_to_weight_dict.keys():
            self._graph[edge[0], edge[1]] = edge_to_weight_dict[edge]

    def __init_sub_grap_wrapper(self, vertices):
        graph_wrapper = GraphWrapper()
        graph_wrapper._graph = self._graph.subgraph(vertices)
        graph_wrapper._number_of_vertices = len(vertices)
        for v_index in range(len(vertices)):
            graph_wrapper._index_to_vertex_dict[v_index] = self._index_to_vertex_dict[vertices[v_index]]
            graph_wrapper._vertex_to_index_dict[self._index_to_vertex_dict[vertices[v_index]]] = v_index
        return graph_wrapper

    def __sub_graph_by_vertices(self, samples):
        sub_edges_list = []
        for e in self._graph.es:
            if e.source in samples and e.target in samples:
                v1 = e.source
                v2 = e.target
                sub_edges_list.append((self._index_to_vertex_dict[v1], self._index_to_vertex_dict[v2]))
        sub_graph_wrapper = GraphWrapper()
        edge_weight_dict = sub_graph_wrapper.__init__edges_list_from_list(sub_edges_list)
        sub_graph_wrapper.__init_graph_by_edges_dict(edge_weight_dict, is_directed=self._graph.is_directed)
        return sub_graph_wrapper

    def load_from_file(self, is_directed=False, file_path='./'):
        edge_to_weight_dict = self.__init_edges_list_from_file(file_path)

        self.__init_graph_by_edges_dict(edge_to_weight_dict, is_directed)

    def load_from_db(self, is_directed=False, file_path=None):
        edge_to_weight_dict = self.__init_edges_list_from_db(file_path=file_path)

        self.__init_graph_by_edges_dict(edge_to_weight_dict, is_directed)

    def save_graph_to_file(self, file_path='./'):
        with open(file_path, 'w') as f:
            for e in self._graph.es:
                v_srg = self._index_to_vertex_dict[e.source]
                v_trg = self._index_to_vertex_dict[e.target]
                f.writelines('{0}\t{1}\t{2}\n'.format(v_srg, v_trg, e["weight"]))

    def degree(self, vertices_list=None):
        vertex_to_degree = {}
        if vertices_list is not None:
            vertex_indexes = [self._vertex_to_index_dict[vertex_name] for vertex_name in vertices_list]
            vertices_degree_in = self._graph.degree(vertices=vertex_indexes, mode="in")
            vertices_degree_out = self._graph.degree(vertices=vertex_indexes, mode="out")
        else:
            vertices_degree_in = self._graph.degree(mode="in")
            vertices_degree_out = self._graph.degree(mode="out")
            vertex_indexes = range(self._number_of_vertices)

        for index in range(len(vertex_indexes)):
            vertex_index = vertex_indexes[index]
            vertex_name = self._index_to_vertex_dict[vertex_index]
            vertex_to_degree[vertex_name] = [vertices_degree_in[index], vertices_degree_out[index]]

        return vertex_to_degree

    def k_coreness(self, vertices_list=None):
        vertex_to_kcore = {}
        vertices_coreness = self._graph.coreness()

        if vertices_list is not None:
            for vertex_name in vertices_list:
                vertex_index = self._vertex_to_index_dict[vertex_name]
                vertex_to_kcore[vertex_name] = vertices_coreness[vertex_index]
        else:
            for vertex_index in range(self._number_of_vertices):
                vertex_name = self._index_to_vertex_dict[vertex_index]
                vertex_to_kcore[vertex_name] = vertices_coreness[vertex_index]

        return vertex_to_kcore

    def page_rank(self, vertices_list=None):
        vertex_to_pagerank = {}
        vertices_pagerank = self._graph.pagerank()

        if vertices_list is not None:
            for vertex_name in vertices_list:
                vertex_index = self._vertex_to_index_dict[vertex_name]
                vertex_to_pagerank[vertex_name] = vertices_pagerank[vertex_index]
        else:
            for vertex_index in range(self._number_of_vertices):
                vertex_name = self._index_to_vertex_dict[vertex_index]
                vertex_to_pagerank[vertex_name] = vertices_pagerank[vertex_index]

        return vertex_to_pagerank

    def closeness(self, vertices_list=None):
        vertex_to_closeness = {}
        if vertices_list is not None:
            vertex_indexes = [self._vertex_to_index_dict[vertex_name] for vertex_name in vertices_list]
            vertices_closeness = self._graph.closeness(vertices=vertex_indexes)
            for index in range(len(vertex_indexes)):
                vertex_index = vertex_indexes[index]
                vertex_name = self._index_to_vertex_dict[vertex_index]
                vertex_to_closeness[vertex_name] = vertices_closeness[index]
        else:
            vertices_closeness = self._graph.closeness()
            for vertex_index in range(self._number_of_vertices):
                vertex_name = self._index_to_vertex_dict[vertex_index]
                vertex_to_closeness[vertex_name] = vertices_closeness[vertex_index]

        return vertex_to_closeness

    def betweenness(self, vertices_list=None):
        vertex_to_betweenness = {}
        if vertices_list is not None:
            vertex_indexes = [self._vertex_to_index_dict[vertex_name] for vertex_name in vertices_list]
            vertices_betweenness = self._graph.betweenness(vertices=vertex_indexes)
            for index in range(len(vertex_indexes)):
                vertex_index = vertex_indexes[index]
                vertex_name = self._index_to_vertex_dict[vertex_index]
                vertex_to_betweenness[vertex_name] = vertices_betweenness[index]
        else:
            vertices_betweenness = self._graph.betweenness()
            for vertex_index in range(self._number_of_vertices):
                vertex_name = self._index_to_vertex_dict[vertex_index]
                vertex_to_betweenness[vertex_name] = vertices_betweenness[vertex_index]

        return vertex_to_betweenness

    def bfs_moments(self, vertices_list=None):
        vertex_to_bfs_moments = {}
        if vertices_list is not None:
            vertex_indexes = [self._vertex_to_index_dict[vertex_name] for vertex_name in vertices_list]
            vertices_bfs_moments = self._bfs.bfs_momemts(self._graph, vertex_indexes)
            for index in range(len(vertex_indexes)):
                vertex_index = vertex_indexes[index]
                vertex_name = self._index_to_vertex_dict[vertex_index]
                vertex_to_bfs_moments[vertex_name] = vertices_bfs_moments[vertex_index]
        else:
            vertices_bfs_moments = self._bfs.bfs_momemts(self._graph)
            for vertex_index in range(self._number_of_vertices):
                vertex_name = self._index_to_vertex_dict[vertex_index]
                vertex_to_bfs_moments[vertex_name] = vertices_bfs_moments[vertex_index]

        return vertex_to_bfs_moments

    def motif(self, vertices_list=None, motif_veriation_folder='./', motif_size=3):
        if vertices_list is not None:
            vertices_list = [self._vertex_to_index_dict[v] for v in vertices_list]

        motif = Motif(self._graph.is_directed(), motif_veriation_folder)
        hist = motif.compute_motif(self._graph, vertices_list, motif_size)

        result_hist = {}
        for v in hist.keys():
            result_hist[self._index_to_vertex_dict[v]] = hist[v]
        return result_hist

    def flow(self, vertices_list=None):
        if vertices_list is not None:
            vertices_list = [self._vertex_to_index_dict[v] for v in vertices_list]
        flow_dict = self._flow.compute_flow(self._graph, vertices_list, threshold=0.1)

        result_dict = {}
        for v in flow_dict:
            result_dict[self._index_to_vertex_dict[v]] = flow_dict[v]
        return result_dict

    def propagatoin_features(self, test_vertices, tags):
        return self._propagation.get_vertices_features_by_neighbors(self.get_edges_list(),
                                                                    self.get_vertices_list(),
                                                                    tags,
                                                                    test_vertices)

    def sample_uniform_from_edges(self, number_of_edges):
        sub_edges_list = random.sample(self.get_edges_list(), number_of_edges)
        sub_graph_wrapper = GraphWrapper()
        edge_weight_dict = sub_graph_wrapper.__init__edges_list_from_list(sub_edges_list)
        sub_graph_wrapper.__init_graph_by_edges_dict(edge_weight_dict, is_directed=self._graph.is_directed)

        return sub_graph_wrapper

    def sample_by_vertices_explore(self, number_of_start_vertices, explore_length):
        base_sample_vertices = [v.index for v in random.sample(self._graph.vs, number_of_start_vertices)]
        vertices = set(base_sample_vertices)
        neighbors = base_sample_vertices
        number_of_round = explore_length
        for i in range(number_of_round):
            next_neighbors = set()
            for v in neighbors:
                vertices.add(v)
                current_neighbors = set(self._graph.neighbors(v, mode='ALL'))
                vertices = vertices.union(current_neighbors)
                next_neighbors = next_neighbors.union(current_neighbors)
            neighbors = next_neighbors

        vertices = list(vertices)
        vertices.sort()
        graph_wrapper = self.__init_sub_grap_wrapper(vertices)

        return graph_wrapper

    def sample_uniform_by_vertices(self, number_of_vertices=2):
        samples = {v.index:0 for v in random.sample(self._graph.vs, number_of_vertices)}
        sub_graph_wrapper = self.__sub_graph_by_vertices(samples)
        return sub_graph_wrapper

    def create_sub_graph(self, vertices_list):
        samples = {}
        for v in vertices_list:
            vertex_index = self._vertex_to_index_dict.get(v)
            if vertex_index != None:
                samples[vertex_index] = 0
        sub_graph_wrapper = self.__sub_graph_by_vertices(samples)
        return sub_graph_wrapper

    def get_max_connected_vertices(self, mode='WEAK'):
        clusters = self._graph.clusters(mode=mode)
        biggest_connected = []
        for c in clusters:
            if len(biggest_connected) < len(c):
                biggest_connected = c
        return [self._index_to_vertex_dict[v_i] for v_i in biggest_connected]

    def get_vertices_list(self):
        return self._vertex_to_index_dict.keys()

    def get_edges_list(self):
        edge_list = [(self._index_to_vertex_dict[edge[0]], self._index_to_vertex_dict[edge[1]])
                     for edge in self._graph.get_edgelist()]
        return edge_list

    def print_vertices_list(self):
        for v in self._graph.vs():
            print v.index
