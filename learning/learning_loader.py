import numpy as np
from learning_object import LearningObject
from sklearn.model_selection import train_test_split


class LearningLoader:
    def __init__(self, directory_path):
        self._vertex_to_features = {}
        self._vertex_to_final_features = {}
        self._vertex_to_tags = {}
        self._base_dir = directory_path
        self._train_vertices = []
        self._test_vertices = []

    @property
    def tags(self):
        return self._vertex_to_tags

    def features(self, vertex):
        return self._vertex_to_final_features[vertex]

    def load_features_from_directory(self, *features_file_names):
        for file_name in features_file_names:
            with open('{0}/{1}'.format(self._base_dir, file_name), 'r') as f:
                lines = f.readlines()
            for line in lines:
                features = line.replace('\n', '').split(',')
                vertex = features[0]
                features = [float(feature) for feature in features[1:]]
                if vertex in self._vertex_to_features:
                    self._vertex_to_features[vertex].extend(features)
                else:
                    self._vertex_to_features[vertex] = features

    def load_tags_from_file(self, tags_file_path):
        tags_file_path = self._base_dir+tags_file_path
        self._vertex_to_tags = {}
        with open(tags_file_path) as tags_file:
            lines = tags_file.readlines()
        for line in lines:
            tags = line.replace('\n', '').split()
            vertex = tags[0]
            tag = tags[1]
            self._vertex_to_tags[vertex] = int(tag)

    def divide_train_test(self, test_size=0.2, test_file_path=None):
        self._test_vertices = []
        self._train_vertices = []
        if test_file_path is None:
            vertices = self._vertex_to_features.keys()
            vertices_train, vertices_test = train_test_split(vertices, test_size=test_size)
            self._train_vertices = vertices_train
            self._test_vertices = vertices_test
            return [vertices_train, vertices_test]
        else:
            test_file_path = self._base_dir+test_file_path
            test_vertices = {}
            with file(test_file_path, 'r') as f:
                for line in f:
                    test_vertices[line.replace('\n', '')] = 1
            for v in self._vertex_to_features:
                if v not in test_vertices:
                    self._train_vertices.append(v)
            self._test_vertices = test_vertices.keys()

    def __zscoring(self, matrix):
        new_matrix = np.asmatrix(matrix)
        minimum = np.asarray(new_matrix.min(0))
        for i in range(minimum.shape[1]):
            if minimum[0, i] > 0:
                new_matrix[:, i] = np.log10(new_matrix[:, i])
            elif minimum[0, i] == 0:
                new_matrix[:, i] = np.log10(new_matrix[:, i] + 0.1)
            if new_matrix[:, i].std() > 0:
                new_matrix[:, i] = (new_matrix[:, i] - new_matrix[:, i].min()) / new_matrix[:, i].std()
        return new_matrix

    def get_learning_object(self, zscoring=True):
        features_matrix = []
        for vertex in self._vertex_to_features:
            if vertex in self._vertex_to_tags and vertex in self._vertex_to_features:
                vertex_features = [vertex]
                vertex_features.append(self._vertex_to_tags[vertex])
                vertex_features.extend(self._vertex_to_features[vertex])
                features_matrix.append(vertex_features)

        features_matrix = np.asmatrix(features_matrix)
        if (zscoring):
            final_matrix = self.__zscoring(features_matrix[:, 2:].astype(float))
        else:
            final_matrix = features_matrix[:, 2:].astype(float)

        test_vertices_dict = {v: 1 for v in self._test_vertices}
        final_test_matrix = []
        final_train_matrix = []
        final_test_tags = []
        final_train_tags = []
        test_vertices = []
        train_vertices = []
        for i in range(features_matrix.shape[0]):
            vertex = features_matrix[i, 0]
            if str(vertex) in test_vertices_dict:
                final_test_matrix.append(final_matrix[i, :].tolist()[0])
                final_test_tags.append(float(features_matrix[i, 1]))
                test_vertices.append(str(vertex))
            else:
                final_train_matrix.append(final_matrix[i, :].tolist()[0])
                final_train_tags.append(float(features_matrix[i, 1]))
                train_vertices.append(str(vertex))
            self._vertex_to_final_features[str(vertex)] = final_matrix[i, :].tolist()[0]

        return LearningObject(test_features_matrix=np.asmatrix(final_test_matrix),
                              test_tags_vector=np.asmatrix(final_test_tags),
                              test_vertices=test_vertices,
                              train_features_matrix=np.asmatrix(final_train_matrix),
                              train_tags_vector=np.asmatrix(final_train_tags),
                              train_vertices=train_vertices)

