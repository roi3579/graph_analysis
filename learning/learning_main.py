from learning_loader import LearningLoader
from learning.classic_ml import ClassicMachineLearning

import sys

dir_path = r'./../data/directed/livejournal/snap0001/'
ll = LearningLoader(directory_path = dir_path)

ll.load_features_from_directory('degrees_750000.txt',
                                'kcore_750000.txt',
                                'page_rank_750000.txt',
                                'closeness_750000.txt',
                                'bfs_moments_750000.txt',
                                'motifs_3_750000.txt')
ll.load_tags_from_file(dir_path+'/doi_750000/music.txt')

learning_object = ll.get_learning_object(zscoring=True)
x = learning_object.features_matrix
y = learning_object.tags_vector
print x.shape
print y.shape
deep = bool(int(sys.argv[1]))
if(deep):
    from learning.deep_learning import DeepLearning
    learning = DeepLearning(learning_object)
    print 'deep'
    learning.run_learning(test_size=0.2)
else:
    learning = ClassicMachineLearning(learning_object)
    algo_name = sys.argv[2]
    print algo_name
    learning.run_learning(test_size=0.2, algo_name=algo_name)

print 'auc train:',learning.evaluate_AUC_train()
print 'auc test:',learning.evaluate_AUC_test()
