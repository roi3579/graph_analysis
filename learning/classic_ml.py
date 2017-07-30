import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.ensemble import AdaBoostClassifier
from sklearn.linear_model import SGDClassifier
from learning_base import LearningBase


class ClassicMachineLearning(LearningBase):
    def run_learning(self, algo_name, test_size=0.3, random_state=None):
        self._divide_test_train(test_size, random_state=random_state)
        clf = None
        if algo_name == 'adaBoost':
            clf = AdaBoostClassifier(n_estimators=100)
        if algo_name == 'RF':
            clf = RandomForestClassifier(n_estimators=1000, criterion="gini", min_samples_split=15, oob_score=True,
                                         class_weight='balanced', max_depth=3)
        if algo_name == 'L-SVM':
            clf = SVC(kernel='linear', class_weight="balanced", C=0.01)
        if algo_name == 'RBF-SVM':
            clf = SVC(class_weight="balanced", C=0.01)
        if algo_name == 'SGD':
            clf = SGDClassifier(alpha=0.0001, average=False, class_weight=None, epsilon=0.1, eta0=0.0,
                                fit_intercept=True, l1_ratio=0.15, learning_rate='optimal', loss='hinge',
                                n_iter=5, n_jobs=1, penalty='l2', power_t=0.5, random_state=None, shuffle=True,
                                verbose=0, warm_start=False)
        if clf is None:
            raise NotImplementedError()

        self._classifier = clf.fit(self._features_train, np.array(self._tags_train).reshape(-1, ))

        return self._classifier
