import numpy as np
from learning_object import LearningObject
import random
from sklearn.model_selection import train_test_split


class LearningLoader:
    def __init__(self, directory_path):
        self._vertex_to_features = {}
        self._vertex_to_tags = {}
        self._base_dir = directory_path
        self._train_vertices = []
        self._test_vertices = []

    @property
    def tags(self):
        return self._vertex_to_tags

    def load_features_from_directory(self, *features_file_names):
        for file_name in features_file_names:
            with open('{0}/{1}'.format(self._base_dir,file_name),'r') as f:
                lines = f.readlines()
            for line in lines:
                features = line.replace('\n','').split(',')
                vertex = features[0]
                features = [float(feature) for feature in features[1:]]
                if vertex in self._vertex_to_features:
                    self._vertex_to_features[vertex].extend(features)
                else:
                    self._vertex_to_features[vertex] = features

    def load_tags_from_file(self, tags_file_path):
        self._vertex_to_tags = {}
        with open(tags_file_path) as tags_file:
            lines = tags_file.readlines()
        for line in lines:
            tags = line.replace('\n', '').split()
            vertex = tags[0]
            tag = tags[1]
            self._vertex_to_tags[vertex] = int(tag)

    def divide_train_test(self, test_size=0.2):
        vertices = self._vertex_to_features.keys()
        vertices_train, vertices_test = train_test_split(vertices, test_size=test_size)
        return [vertices_train, vertices_test]

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
        features_matrix =[]
        for vertex in self._vertex_to_features:
            vertex_features = [vertex]
            if vertex in self._vertex_to_tags:
                vertex_features.append(self._vertex_to_tags[vertex])
            else:
                vertex_features.append(0)
            vertex_features.extend(self._vertex_to_features[vertex])
            features_matrix.append(vertex_features)

        features_matrix = np.asmatrix(features_matrix)
        if (zscoring):
            final_matrix = self.__zscoring(features_matrix[:,2:].astype(float))
        else:
            final_matrix = features_matrix[:,2:].astype(float)
        tags_vector = features_matrix[:,1:2].astype(float)
        return LearningObject(final_matrix, tags_vector)

    def get_test_object(self,zscoring=True, vertices_list=[]):
        return