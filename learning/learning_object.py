

class LearningObject:
    def __init__(self, features_matrix, tags_vector):
        self._features_matrix = features_matrix
        self._tags_vector = tags_vector

    @property
    def features_matrix(self):
        return self._features_matrix

    @property
    def tags_vector(self):
        return self._tags_vector
