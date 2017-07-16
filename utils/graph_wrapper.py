from igraph import Graph
import pymysql
from graph_algos.bfs import BFS
import json


class GraphWrapper:
    def __init__(self):
        self._graph = None
        self._vertex_to_index_dict = {}
        self._index_to_vertex_dict = {}
        self._number_of_vertices = 0
        self._bfs = BFS()

    def __init_edges_list_from_file(self, file_path):
        edge_to_weight_dict = {}
        lines = open(file_path).readlines()
        for line in lines:
            words = line.replace('\n', '').replace('\r','').replace('\t',' ').split(' ')
            v_src = words[0]
            v_trg = words[1]
            weight = float(words[2])
            self.__add_new_vertex(v_src)
            self.__add_new_vertex(v_trg)
            src_index = self._vertex_to_index_dict[v_src]
            trg_index = self._vertex_to_index_dict[v_trg]
            edge_to_weight_dict[(src_index, trg_index)] = weight

        return edge_to_weight_dict

    def __init_edges_list_from_db(self,file_path):
        edge_to_weight_dict ={}
        with open(file_path,'r') as f:
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
            count +=1
            self.__add_new_vertex(v_src)
            self.__add_new_vertex(v_trg)
            src_index = self._vertex_to_index_dict[v_src]
            trg_index = self._vertex_to_index_dict[v_trg]
            edge_to_weight_dict[(src_index, trg_index)] = 1

        print count
        cnx.close()

        return edge_to_weight_dict

    def __add_new_vertex(self, vertex_name):
        if not self._vertex_to_index_dict.has_key(vertex_name):
            self._vertex_to_index_dict[vertex_name] = self._number_of_vertices
            self._index_to_vertex_dict[self._number_of_vertices] = vertex_name
            self._number_of_vertices += 1

    def __init_graph_by_edges_list(self, edge_to_weight_dict, is_directed):
        self._graph = Graph(directed=is_directed)
        self._graph.add_vertices(self._number_of_vertices)
        self._graph.add_edges(edge_to_weight_dict.keys())
        self._graph.es["weight"] = 1.0
        for edge in edge_to_weight_dict.keys():
            self._graph[edge[0], edge[1]] = edge_to_weight_dict[edge]

    def load_from_file(self, is_directed=False, file_path='./'):
        edge_to_weight_dict = self.__init_edges_list_from_file(file_path)

        self.__init_graph_by_edges_list(edge_to_weight_dict, is_directed)

    def load_from_db(self,is_directed=False,file_path=None):
        edge_to_weight_dict = self.__init_edges_list_from_db(file_path=file_path)

        self.__init_graph_by_edges_list(edge_to_weight_dict, is_directed)

    def degree(self,vertices_list=None):
        vertex_to_degree = {}
        if vertices_list is not None:
            vertex_indexes = [self._vertex_to_index_dict[vertex_name] for vertex_name in vertices_list]
            vertices_degree_in = self._graph.degree(vertices=vertex_indexes,mode="in")
            vertices_degree_out = self._graph.degree(vertices=vertex_indexes,mode="out")
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

    def bfs_moments(self ,vertices_list=None):
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

    def get_vertices_list(self):
        return self._vertex_to_index_dict.keys()

    def print_edges_list(self):
        for edge in self._graph.get_edgelist():
            print edge
            print self._index_to_vertex_dict[edge[0]], \
                self._index_to_vertex_dict[edge[1]], \
                self._graph[edge[0], edge[1]]

    def print_vertices_list(self):
        for v in self._graph.vs():
            print v.index