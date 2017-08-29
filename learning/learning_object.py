

class LearningObject:
    def __init__(self, train_features_matrix, train_tags_vector, test_features_matrix, test_tags_vector):
        self._train_features_matrix = train_features_matrix
        self._train_tags_vector = train_tags_vector.reshape(-1, 1)
        self._test_features_matrix = test_features_matrix
        self._test_tags_vector = test_tags_vector.reshape(-1, 1)

    @property
    def train_features_matrix(self):
        return self._train_features_matrix

    @property
    def train_tags_vector(self):
        return self._train_tags_vector

    @property
    def test_features_matrix(self):
        return self._test_features_matrix

    @property
    def test_tags_vector(self):
        return self._test_tags_vector