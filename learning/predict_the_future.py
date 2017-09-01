import pickle
from learning_loader import LearningLoader
from classic_ml import ClassicMachineLearning
import os
from keras.models import load_model
import sys

def get_snap(i):
    if i <10:
        return '000'+str(i)
    return '00'+str(i)

def init_vertex_to_tag_to_snap(dir_path,doi,sample_size):
    snap_to_vertex_to_tag = {}
    for i in range(1, 20):
        snap = get_snap(i)
        leaning_loader = LearningLoader(directory_path='{0}/snap{1}/'.format(dir_path, snap))
        leaning_loader.load_tags_from_file('/doi_{0}/{1}'.format(sample_size, doi))
        snap_to_vertex_to_tag[i] = leaning_loader.tags

    return snap_to_vertex_to_tag



dir_path =  r'./../data/directed/livejournal/'
sample_size = 750000
dois = os.listdir('{0}/snap0001/doi_{1}'.format(dir_path,sample_size))
dois.remove('accountstypes.txt')
for doi in dois:
    deep = False
    if deep:
        clf = load_model('{0}/snap{1}/deep_clf_{2}/{3}_deep.pkl'.format(dir_path,'0001',sample_size,doi.replace('.txt','')))
    else:
        with file('{0}/snap{1}/clf_{2}/RF_{3}'.format(dir_path,'0001',sample_size,doi)) as f:
            clf =pickle.load(f)
    print doi
    snap = '0001'
    print snap
    leaning_loader = LearningLoader(directory_path='{0}/snap{1}/'.format(dir_path, snap))
    leaning_loader.load_features_from_directory('degrees_{0}.txt'.format(sample_size),
                                                'kcore_{0}.txt'.format(sample_size),
                                                'page_rank_{0}.txt'.format(sample_size),
                                                'closeness_{0}.txt'.format(sample_size),
                                                'bfs_moments_{0}.txt'.format(sample_size),
                                                'motifs_3_{0}.txt'.format(sample_size),)
                                                # 'motifs_4_{0}.txt'.format(sample_size),
                                                # 'propagation_{0}_20/propagation_{1}'.format(sample_size,doi))

    leaning_loader.load_tags_from_file('/doi_{0}/{1}'.format(sample_size, doi))
    leaning_loader.divide_train_test(test_file_path='test_20_{0}.txt'.format(sample_size))
    learning_object = leaning_loader.get_learning_object(zscoring=True)

    vertex_to_tags = leaning_loader.tags
    count_diff = 0

    ml = ClassicMachineLearning(learning_object)

    snap_to_vertex_to_tag = init_vertex_to_tag_to_snap(dir_path,doi,sample_size)

    with open('{0}/snap{1}/prediction_result_{2}/predict_{3}'.format(dir_path, snap, sample_size, doi), 'w') as f:
        prediction = clf.predict(learning_object.test_features_matrix)

        for i in range(len(prediction)):
            vertex = learning_object.test_vertices[i]
            predict_tag = prediction[i]
            f.writelines('{0},{1}'.format(vertex, predict_tag))
            for i in range(1, 20):
                vertex_to_tags = snap_to_vertex_to_tag[i]
                real_tag = vertex_to_tags.get(vertex)
                if real_tag is None:
                    real_tag = -1
                f.writelines(',{0}'.format(real_tag))
            f.writelines('\n')