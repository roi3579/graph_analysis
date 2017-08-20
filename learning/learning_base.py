import numpy as np
from sklearn import metrics
from sklearn.model_selection import train_test_split


class LearningBase:
    def __init__(self, learning_object):
        self._features_train = learning_object.train_features_matrix
        self._tags_train = learning_object.train_tags_vector.reshape(-1, 1)
        self._features_test = learning_object.test_features_matrix
        self._tags_test = learning_object.test_tags_vector.reshape(-1, 1)
        self._classifier = None

    def evaluate_AUC_test(self):
        return self.evaluate_AUC_general(self._classifier, self._features_test, self._tags_test)

    def evaluate_AUC_train(self):
        return self.evaluate_AUC_general(self._classifier, self._features_train, self._tags_train)

    def evaluate_AUC_general(self, classifier, features, tags):
        predictions = classifier.predict(features)
        train_fpr, train_tpr, thresholds = metrics.roc_curve(tags, predictions)
        auc = np.trapz(train_tpr, train_fpr)
        return auc

    def evaluate_confusion_metric_test(self):
        y_pred = self._classifier.predict_proba(self._features_test)
        y_pred = [np.argmax(lst) for lst in y_pred]
        y_true = [int(i) for i in self._tags_test]
        confusion_matrix_result = metrics.confusion_matrix(y_true,y_pred)
        print confusion_matrix_result
        confusion_matrix_result = confusion_matrix_result.astype('float') / confusion_matrix_result.sum(axis=1)[:, np.newaxis]
        return confusion_matrix_result

    def evaluate_confusion_metric_train(self):
        y_pred = self._classifier.predict_proba(self._features_train)
        y_pred = [np.argmax(lst) for lst in y_pred]
        y_true = [int(i) for i in self._tags_train]
        confusion_matrix_result = metrics.confusion_matrix(y_true, y_pred)
        return confusion_matrix_result

    def evaluate_f1_score(self):
        y_pred = self._classifier.predict_proba(self._features_test)
        y_true = self._tags_test
        precision, recall, thresholds = metrics.precision_recall_curve(y_true,y_pred)
        x = np.multiply(precision, recall) / np.sum([precision, recall], axis=0)
        score = 2*np.amax(x[np.logical_not(np.isnan(x))])
        return score

    # def write_coloring_file(self, node_to_zscoringfeatures, vertex_to_tags, file_name = None):
    #     if(file_name != None):
    #         f = open(file_name,'w')
    #
    #     coloring_node = []
    #     for n in node_to_zscoringfeatures:
    #         node_features = node_to_zscoringfeatures[n]
    #         prob = self.classifier.predict_proba(node_features)
    #         coloring_node.append((n ,prob))
    #         if(file_name != None):
    #             line = str(n) +' ' + str(vertex_to_tags[n])
    #             for p in prob:
    #                 line += ',' + str(p)
    #             f.writelines(line + '\n')
    #
    #     if (file_name != None):
    #         f.close()
    #     return coloring_node
