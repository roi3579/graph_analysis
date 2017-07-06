from igraph import Graph
from mysql.connector import (connection)


class GraphWrapper:
    def __init__(self):
        self._graph = None
        self._vertex_to_index_dict = {}
        self._index_to_vertex_dict = {}
        self._number_of_vertices = 0

    def __init_edges_list_from_file(self, file_path):
        edge_to_weight_dict = {}
        lines = open(file_path).readlines()
        for line in lines:
            words = line.replace('\n', '').split(' ')
            v_src = words[0]
            v_trg = words[1]
            weight = float(words[2])
            self.__add_new_vertex(v_src)
            self.__add_new_vertex(v_trg)
            src_index = self._vertex_to_index_dict[v_src]
            trg_index = self._vertex_to_index_dict[v_trg]
            edge_to_weight_dict[(src_index, trg_index)] = weight

        return edge_to_weight_dict

    def __init_edges_list_from_db(self):
        edge_to_weight_dict ={}
        cnx = connection.MySQLConnection(user='naamanr', password='3579',
                                         host='132.71.121.215',
                                         database='ljhistory')

        cursor = cnx.cursor()

        query = "select f.Source,f.Dest from ljhistory.friends_0001 f where f.Source!= f.Dest"
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



    def load_from_db(self,is_directed=False):
        edge_to_weight_dict = self.__init_edges_list_from_db()

        self.__init_graph_by_edges_list(edge_to_weight_dict, is_directed)

    def coreness(self, vertices_list=None):
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

    def print_edges_list(self):
        for edge in self._graph.get_edgelist():
            print self._index_to_vertex_dict[edge[0]], \
                self._index_to_vertex_dict[edge[1]], \
                self._graph[edge[0], edge[1]]
