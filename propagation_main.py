from utils.graph_wrapper import GraphWrapper
from utils.features_saver import FeatureSaver
from learning.learning_loader import LearningLoader
from datetime import datetime
import os
import multiprocessing
import sys


def write_log(s):
    print s, datetime.now()

def propagation_by_snap_number(i):

    graph_wrapper = GraphWrapper()
    feature_saver = FeatureSaver()
    test_size = 0.2
    if i < 10:
        snap = '000' + str(i)
    else:
        snap = '00' + str(i)
    print snap
    sample_size = 750000
    output_dir = './data/directed/livejournal/snap{0}/'.format(snap)
    leaning_loader = LearningLoader(directory_path=output_dir)
    leaning_loader.load_features_from_directory('degrees_{0}.txt'.format(sample_size))

    # train_vertices, test_vertices = leaning_loader.divide_train_test(test_size=test_size)
    test_vertices = []
    with file(output_dir + '/test_{0}_{1}.txt'.format(int(test_size * 100), sample_size)) as f:
        for l in f:
            test_vertices.append(l.replace('\n', ''))

    doi_dir = output_dir + '/doi_{0}/'.format(sample_size)
    dois = os.listdir(doi_dir)
    # dois = ['music.txt']
    for doi in dois:
        print doi
        leaning_loader.load_tags_from_file('/doi_{0}/{1}'.format(sample_size, doi))
        tags = leaning_loader.tags
        # output_dir = './data/roi_data/'

        graph_wrapper.load_from_file(is_directed=True,
                                     file_path=output_dir + 'uniform_sample_p_{0}.txt'.format(sample_size))
        print 'edges:', len(graph_wrapper.get_edges_list())
        print 'vertices:', len(graph_wrapper.get_vertices_list())

        write_log('features propagation')
        propagation = graph_wrapper.propagatoin_features(test_vertices, tags)
        if not os.path.exists(output_dir + '/propagation_{0}_{1}/'):
            os.makedirs(output_dir + '/propagation_{0}_{1}/')
        propagation_dir = output_dir + '/propagation_{0}_{1}/'.format(sample_size, int(test_size * 100))
        if not os.path.exists(propagation_dir):
            os.makedirs(propagation_dir)
        feature_saver.save_vertex_features_to_file(propagation, propagation_dir + '/propagation_{0}'.format(doi))



pool = multiprocessing.Pool(19)
pool.map(propagation_by_snap_number,range(2,20))
# for i in range(2,20):
#    propagation_by_snap_number(i)
