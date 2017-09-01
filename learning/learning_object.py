

class LearningObject:
    def __init__(self, train_features_matrix, train_tags_vector, train_vertices,
                 test_features_matrix, test_tags_vector, test_vertices):
        self._train_features_matrix = train_features_matrix
        self._train_tags_vector = train_tags_vector.reshape(-1, 1)
        self._train_vertices = train_vertices
        self._test_features_matrix = test_features_matrix
        self._test_tags_vector = test_tags_vector.reshape(-1, 1)
        self._test_vertices = test_vertices

    @property
    def train_features_matrix(self):
        return self._train_features_matrix

    @property
    def train_tags_vector(self):
        return self._train_tags_vector

    @property
    def train_vertices(self):
        return self._train_vertices

    @property
    def test_features_matrix(self):
        return self._test_features_matrix

    @property
    def test_tags_vector(self):
        return self._test_tags_vector

    @property
    def test_vertices(self):
        return self._test_vertices

