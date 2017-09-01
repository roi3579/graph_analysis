import pickle
from learning_loader import LearningLoader
from classic_ml import ClassicMachineLearning
from keras.models import load_model
import os
import numpy as np

def get_snap(i):
    if i <10:
        return '000'+str(i)
    return '00'+str(i)

def init_vertex_to_tag_to_snap(dir_path,doi,):
    leaning_loader = LearningLoader(directory_path='{0}/snap{1}/'.format(dir_path, snap))
    leaning_loader.load_tags_from_file('/doi_{0}/{1}'.format(sample_size, doi))
    leaning_loader.divide_train_test(test_file_path='test_20_{0}.txt'.format(sample_size))

dir_path = r'./../data/directed/livejournal/'
sample_size = 750000
dois = os.listdir('{0}/snap0001/doi_{1}'.format(dir_path,sample_size))
dois.remove('accountstypes.txt')
file_result = file(r'./../data/directed/livejournal/snap0001/auc_with_same_clf.txt','w')
for doi in dois:
    deep = False
    if deep:
        clf = load_model('{0}/snap{1}/deep_clf_{2}/{3}_deep.pkl'.format(dir_path, '0001', sample_size, doi.replace('.txt', '')))
    else:
        with file('{0}/snap{1}/clf_{2}/RF_{3}'.format(dir_path,'0001',sample_size,doi)) as f:
            clf =pickle.load(f)
    file_result.writelines(doi+'\n')
    print doi
    # ran = [1, 2, 10, 19]
    for i in range(1, 19):
        snap = get_snap(i)
        file_result.writelines(snap +'\n')
        print snap
        leaning_loader = LearningLoader(directory_path='{0}/snap{1}/'.format(dir_path, snap))
        leaning_loader.load_features_from_directory('degrees_{0}.txt'.format(sample_size),
                                                    'kcore_{0}.txt'.format(sample_size),
                                                    'page_rank_{0}.txt'.format(sample_size),
                                                    'closeness_{0}.txt'.format(sample_size),
                                                    'bfs_moments_{0}.txt'.format(sample_size),
                                                    'motifs_3_{0}.txt'.format(sample_size),
                                                    'motifs_4_{0}.txt'.format(sample_size),
                                                    'propagation_{0}_20/propagation_{1}'.format(sample_size,doi))

        leaning_loader.load_tags_from_file('/doi_{0}/{1}'.format(sample_size, doi))
        leaning_loader.divide_train_test(test_file_path='test_20_{0}.txt'.format(sample_size))
        learning_object = leaning_loader.get_learning_object(zscoring=True)

        vertex_to_tags = leaning_loader.tags
        count_diff = 0

        ml = ClassicMachineLearning(learning_object)
        auc = ml.evaluate_AUC_general(clf, learning_object.test_features_matrix, learning_object.test_tags_vector)

        file_result.writelines('auc:{0}\n'.format(auc))
        print auc
        file_result.flush()