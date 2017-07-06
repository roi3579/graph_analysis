
class FeatureSaver:

    def save_vertex_features_to_file(self, vertex_to_features_dict, file_path):
        with open(file_path,'w') as f:
            for vertex in vertex_to_features_dict:
                f.writelines('{0} {1}\n'.format(vertex,str(vertex_to_features_dict[vertex])))



