from learning_loader import LearningLoader
from classic_ml import ClassicMachineLearning
import sys



def get_learning_loader(dir_path):
    leaning_loader = LearningLoader(directory_path=dir_path)
    leaning_loader.load_features_from_directory('degrees_750000.txt',
                                    'kcore_750000.txt',
                                    'page_rank_750000.txt',
                                    'closeness_750000.txt',
                                    'bfs_moments_750000.txt',
                                    'motifs_3_750000.txt',
                                    'motifs_4_750000.txt')
    leaning_loader.load_tags_from_file(dir_path+'/doi_750000/music.txt')

    return leaning_loader



dir_path = r'./../data/directed/livejournal/snap0001/'
learning_loader = get_learning_loader(dir_path)
learning_object = learning_loader.get_learning_object(zscoring=True)
x = learning_object.features_matrix
y = learning_object.tags_vector
print x.shape
print y.shape
deep = bool(int(sys.argv[1]))
# deep = False
if(deep):
    from deep_learning import DeepLearning
    learning = DeepLearning(learning_object)
    print 'deep'
    learning.run_learning(test_size=0.2)
else:
    learning = ClassicMachineLearning(learning_object)
    algo_name = sys.argv[2]
    # algo_name = 'RF'
    print algo_name
    clf = learning.run_learning(test_size=0.2, algo_name=algo_name)

print 'auc train:',learning.evaluate_AUC_train()
print 'auc test:',learning.evaluate_AUC_test()
# print 'auc test:',learning.evaluate_AUC_test()

dir_path = r'./../data/directed/livejournal/snap0002/'
learning_loader2 = get_learning_loader(dir_path)
learning_object2 = learning_loader2.get_learning_object(zscoring=True)
print 'auc snap 0002:',learning.evaluate_AUC_general(clf, learning_object2.features_matrix, learning_object2.tags_vector)

dir_path = r'./../data/directed/livejournal/snap0010/'
learning_loader3 = get_learning_loader(dir_path)
learning_object3 = learning_loader3.get_learning_object(zscoring=True)
print 'auc snap 0010:',learning.evaluate_AUC_general(clf, learning_object3.features_matrix, learning_object3.tags_vector)

dir_path = r'./../data/directed/livejournal/snap0019/'
learning_loader4 = get_learning_loader(dir_path)
learning_object4 = learning_loader4.get_learning_object(zscoring=True)
print 'auc snap0019:',learning.evaluate_AUC_general(clf, learning_object4.features_matrix, learning_object4.tags_vector)
