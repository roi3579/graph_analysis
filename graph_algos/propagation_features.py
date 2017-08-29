
class Propagation:
    def __init__(self):
        pass

    def get_vertices_features_by_neighbors(self, edges_list, vertices_list, tags, test_vertices):
        vertices_to_class_dict = self.__init_vertex_to_class(edges_list, vertices_list, tags, test_vertices)
        result_propagation_dict = {}
        for v in vertices_to_class_dict:
            result_propagation_dict[v] = vertices_to_class_dict[v]['out']+vertices_to_class_dict[v]['in']
        return result_propagation_dict

    def __init_vertex_to_class(self, edges_list, vertices_list, tags, test_vertices):
        vertices_to_class_dict = {}
        class_to_place, number_of_classes = self.__init_classes_to_plcae(tags)
        for v in vertices_list:
            vertices_to_class_dict[v] = {'in': [0] * number_of_classes, 'out': [0] * number_of_classes}
        self.__compute_vertex_to_class(class_to_place, edges_list, tags, test_vertices, vertices_to_class_dict)
        return vertices_to_class_dict

    def __compute_vertex_to_class(self, class_to_place, edges_list, tags, test_vertices, vertices_to_class_dict):
        count = 0
        len_edges = len(edges_list)
        for e in edges_list:
            if count % 100000 == 0:
                print count, len_edges
            count +=1
            src = e[0]
            trg = e[1]
            if src not in test_vertices:
                src_tag = tags[src]
                vertices_to_class_dict[trg]['in'][class_to_place[src_tag]] += 1
            if trg not in test_vertices:
                trg_tag = tags[trg]
                vertices_to_class_dict[src]['out'][class_to_place[trg_tag]] += 1

    def __init_classes_to_plcae(self, tags):
        type_of_classes = set(tags.values())
        number_of_classes = 0
        class_to_place = {}
        for tag in type_of_classes:
            class_to_place[tag] = number_of_classes
            number_of_classes += 1
        return class_to_place, number_of_classes