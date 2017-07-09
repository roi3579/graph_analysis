from utils.graph_wrapper import GraphWrapper
from utils.features_saver import FeatureSaver
import datetime

graph_wrapper = GraphWrapper()
feature_saver = FeatureSaver()

graph_wrapper.load_from_file(is_directed=True,file_path='./data/roi_data/input.txt')
# graph_wrapper.print_vertices_list()
# graph_wrapper.print_edges_list()

kcore_features= graph_wrapper.k_coreness()
# print kcore_features
feature_saver.save_vertex_features_to_file(kcore_features,'./data/roi_data/kcore.txt')

pagerank_features= graph_wrapper.page_rank()
# print pagerank_features
feature_saver.save_vertex_features_to_file(pagerank_features, './data/roi_data/page_rank.txt')

closeness_features= graph_wrapper.closeness()
# print closeness_features
feature_saver.save_vertex_features_to_file(closeness_features, './data/roi_data/closeness.txt')

betweenness_features= graph_wrapper.betweenness()
# print betweenness_features
feature_saver.save_vertex_features_to_file(betweenness_features, './data/roi_data/betweenness.txt')

bfs_moments= graph_wrapper.bfs_moments()
# print bfs_moments
feature_saver.save_vertex_features_to_file(bfs_moments, './data/roi_data/bfs_moments.txt')




print 'start graph',datetime.datetime.now()
graph_wrapper = GraphWrapper()
base_folder = './data/directed/livejournal/snap0001'
input_path = base_folder+'/input.json'
graph_wrapper.load_from_db(is_directed=True,file_path=input_path)
# graph_wrapper.print_edges_list()

print 'start kcore', datetime.datetime.now()
kcore_features= graph_wrapper.k_coreness()
print 'start write', datetime.datetime.now()
# print kcore_features

feature_saver.save_vertex_features_to_file(kcore_features,base_folder+'/kcore.txt')
print 'start page',datetime.datetime.now()

pagerank_features= graph_wrapper.page_rank()
print 'start write', datetime.datetime.now()
# print pagerank_features
feature_saver.save_vertex_features_to_file(pagerank_features, base_folder + '/page_rank.txt')

print 'start closeness',datetime.datetime.now()
closeness_features= graph_wrapper.page_rank()
print 'start write', datetime.datetime.now()
# print pagerank_features
feature_saver.save_vertex_features_to_file(closeness_features, base_folder + '/closeness.txt')
print 'done write', datetime.datetime.now()












