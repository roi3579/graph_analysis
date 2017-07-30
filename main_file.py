from utils.graph_wrapper import GraphWrapper
from utils.features_saver import FeatureSaver
from datetime import datetime
import sys

def write_log(s):
    print s, datetime.now()

i = int(sys.argv[1])
if i<10:
    snap = '000' +str(i)
else:
    snap = '00' + str(i)

# sample_size = 500000
sample_size = int(sys.argv[2])

output_dir = './data/directed/livejournal/snap{0}/'.format(snap)
graph_wrapper = GraphWrapper()
feature_saver = FeatureSaver()

graph_wrapper.load_from_file(is_directed=True, file_path='./data/directed/livejournal/snap{0}/uniform_sample_p_{1}.txt'.format(snap,sample_size))
print 'edges:',len(graph_wrapper.get_edges_list())
print 'vertices:',len(graph_wrapper.get_vertices_list())

write_log('start degree')
degrees = graph_wrapper.degree()
feature_saver.save_vertex_features_to_file(degrees, output_dir+'/degrees_{0}.txt'.format(sample_size))

write_log('start k-core')
kcore_features= graph_wrapper.k_coreness()
feature_saver.save_vertex_features_to_file(kcore_features, output_dir+'/kcore_{0}.txt'.format(sample_size))

write_log('start page-rank')
pagerank_features= graph_wrapper.page_rank()
feature_saver.save_vertex_features_to_file(pagerank_features, output_dir+'/page_rank_{0}.txt'.format(sample_size))

write_log('start closeness')
closeness_features= graph_wrapper.closeness()
feature_saver.save_vertex_features_to_file(closeness_features, output_dir+'/closeness_{0}.txt'.format(sample_size))

# write_log('start betweenness')
# betweenness_features= graph_wrapper.betweenness()
# feature_saver.save_vertex_features_to_file(betweenness_features, output_dir+'/betweenness.txt')

write_log('start bfs')
bfs_moments, flows, ab  = graph_wrapper.bfs()
feature_saver.save_vertex_features_to_file(bfs_moments, output_dir+'/bfs_moments_{0}.txt'.format(sample_size))
feature_saver.save_vertex_features_to_file(bfs_moments, output_dir+'/flows_{0}.txt'.format(sample_size))
feature_saver.save_vertex_features_to_file(bfs_moments, output_dir+'/ab_{0}.txt'.format(sample_size))

write_log('start motif 3')
motifs = graph_wrapper.motif(vertices_list=None, motif_veriation_folder='./graph_algos/motifs_veriation',motif_size=3)
feature_saver.save_vertex_features_to_file(motifs, output_dir+'/motifs_3_{0}.txt'.format(sample_size))

write_log('start motif 4')
motifs = graph_wrapper.motif(vertices_list=None, motif_veriation_folder='./graph_algos/motifs_veriation',motif_size=4)
feature_saver.save_vertex_features_to_file(motifs, output_dir+'/motifs_4_{0}.txt'.format(sample_size))

# print 'start flow',datetime.datetime.now()
# flows = graph_wrapper.flow()
# feature_saver.save_vertex_features_to_file(flows, output_dir+'/flow.txt')
# print 'finish',datetime.datetime.now()
