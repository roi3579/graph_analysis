
class FeatureSaver:
    def save_vertex_features_to_file(self, vertex_to_features_dict, file_path):
        with open(file_path,'w') as f:
            for vertex in vertex_to_features_dict:
                features = vertex_to_features_dict[vertex]
                if type(features) is list:
                    features = ','.join([str(feature) for feature in features])
                f.writelines('{0},{1}\n'.format(vertex, features))

    def save_vertices_to_file(self, file_path, vertices):
        with open(file_path, 'w') as f:
            for v in vertices:
                f.writelines('{0}\n'.format(v))
