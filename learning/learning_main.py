from learning_loader import LearningLoader
from classic_ml import ClassicMachineLearning
import os
import pickle
# import sys


def get_learning_loader(dir_path, doi, sample_size):
    leaning_loader = LearningLoader(directory_path=dir_path)
    leaning_loader.load_features_from_directory('degrees_{0}.txt'.format(sample_size),
                                                'kcore_{0}.txt'.format(sample_size),
                                                'page_rank_{0}.txt'.format(sample_size),
                                                'closeness_{0}.txt'.format(sample_size),
                                                'bfs_moments_{0}.txt'.format(sample_size),
                                                'motifs_3_{0}.txt'.format(sample_size),
                                                'propagation_{0}_20/propagation_{1}'.format(sample_size,doi))
    leaning_loader.load_tags_from_file('/doi_{0}/{1}'.format(sample_size, doi))
    leaning_loader.divide_train_test(test_file_path='test_20_{0}.txt'.format(sample_size))
    return leaning_loader

sample_size = 750000
dir_path = r'./../data/directed/livejournal/snap0001/'
dois = os.listdir(dir_path +'/doi_{0}/'.format(sample_size))
with file(dir_path+'learning_resuls.txt','w') as result_file:
    for doi in dois:
        if doi == 'accountstypes.txt':
            continue
        print doi
        result_file.writelines('{0}\n'.format(doi))
        learning_loader = get_learning_loader(dir_path, doi, sample_size)
        learning_object = learning_loader.get_learning_object(zscoring=True)
        x = learning_object.train_features_matrix
        y = learning_object.train_tags_vector
        print x.shape
        print y.shape
        # deep = bool(int(sys.argv[1]))
        deep = False
        # deep = True
        if(deep):
            from deep_learning import DeepLearning
            learning = DeepLearning(learning_object)
            print 'deep'
            learning.run_learning(test_size=0.2)
        else:
            algos = ['adaBoost', 'RF', 'L-SVM', 'RBF-SVM', 'SGD']
            for algo_name in algos:
                learning = ClassicMachineLearning(learning_object)
                print algo_name
                result_file.writelines('{0}\n'.format(algo_name))
                clf = learning.run_learning(algo_name=algo_name)
                if algo_name == 'RF':
                    print clf.feature_importances_
                    result_file.writelines('{0}\n'.format(clf.feature_importances_))

                auc_train = learning.evaluate_AUC_train()
                print 'auc train:', auc_train
                result_file.writelines('auc train: {0}\n'.format(auc_train))
                auc_test = learning.evaluate_AUC_test()
                result_file.writelines('auc test: {0}\n'.format(auc_test))
                print 'auc test:', auc_test
                result_file.flush()
                with file('{0}/clf_{1}/{2}_{3}'.format(dir_path,sample_size,algo_name,doi),'w') as pickle_file:
                    pickle.dump(clf,file=pickle_file)

# dir_path = r'./../data/directed/livejournal/snap0002/'
# learning_loader2 = get_learning_loader(dir_path)
# learning_object2 = learning_loader2.get_learning_object(zscoring=True)
# print 'auc snap 0002:',learning.evaluate_AUC_general(clf, learning_object2.features_matrix, learning_object2.tags_vector)
#
# dir_path = r'./../data/directed/livejournal/snap0010/'
# learning_loader3 = get_learning_loader(dir_path)
# learning_object3 = learning_loader3.get_learning_object(zscoring=True)
# print 'auc snap 0010:',learning.evaluate_AUC_general(clf, learning_object3.features_matrix, learning_object3.tags_vector)
#
# dir_path = r'./../data/directed/livejournal/snap0019/'
# learning_loader4 = get_learning_loader(dir_path)
# learning_object4 = learning_loader4.get_learning_object(zscoring=True)
# print 'auc snap0019:',learning.evaluate_AUC_general(clf, learning_object4.features_matrix, learning_object4.tags_vector)
