from utils.graph_wrapper import GraphWrapper
from utils.features_saver import FeatureSaver
import datetime

graph_wrapper = GraphWrapper()
feature_saver = FeatureSaver()

graph_wrapper.load_from_file(is_directed=True,file_path='./data/roi_data/input.txt')

kcore_features= graph_wrapper.coreness()
# print kcore_features
feature_saver.save_vertex_features_to_file(kcore_features,'./data/roi_data/kcore.txt')

pagerank_features= graph_wrapper.page_rank()
# print pagerank_features
feature_saver.save_vertex_features_to_file(pagerank_features,'./data/roi_data/page_rank.txt')

print 'start graph',datetime.datetime.now()
graph_wrapper = GraphWrapper()
graph_wrapper.load_from_db(is_directed=True)
# graph_wrapper.print_edges_list()

print 'start kcore', datetime.datetime.now()
kcore_features= graph_wrapper.coreness()
print 'start write', datetime.datetime.now()
# print kcore_features
feature_saver.save_vertex_features_to_file(kcore_features,'./data/roi_data/kcore.txt')
print 'start page',datetime.datetime.now()

pagerank_features= graph_wrapper.page_rank()
print 'start write', datetime.datetime.now()
# print pagerank_features
feature_saver.save_vertex_features_to_file(pagerank_features,'./data/roi_data/page_rank.txt')
print 'done write', datetime.datetime.now()









