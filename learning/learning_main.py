from learning_loader import LearningLoader
from classic_ml import ClassicMachineLearning

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

classic_ml = ClassicMachineLearning(learning_object)
algo_name = 'RF1'
print algo_name
classic_ml.run_learning(algo_name=algo_name,test_size=0.2)
print 'auc train:',classic_ml.evaluate_AUC_train()
print 'auc test:',classic_ml.evaluate_AUC_test()
