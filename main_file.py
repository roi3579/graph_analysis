from utils.graph_wrapper import GraphWrapper
from utils.features_saver import FeatureSaver
import datetime
import random
import sys

graph_wrapper = GraphWrapper()
feature_saver = FeatureSaver()

# graph_wrapper.load_from_file(is_directed=True,file_path='./data/roi_data/input.txt')
graph_wrapper.load_from_file(is_directed=True,file_path='./data/roi_data/cora.txt')
# graph_wrapper.print_vertices_list()
# graph_wrapper.print_edges_list()

kcore_features= graph_wrapper.k_coreness()
# print kcore_features
feature_saver.save_vertex_features_to_file(kcore_features, './data/roi_data/kcore.txt')

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

degrees = graph_wrapper.degree()
# print bfs_moments
feature_saver.save_vertex_features_to_file(degrees, './data/roi_data/degrees.txt')

motifs = graph_wrapper.motif(vertices_list=None, motif_veriation_folder='./graph_algos/motifs_veriation',motif_size=3)
feature_saver.save_vertex_features_to_file(motifs, './data/roi_data/motifs_3.txt')

motifs = graph_wrapper.motif(vertices_list=None, motif_veriation_folder='./graph_algos/motifs_veriation',motif_size=4)
feature_saver.save_vertex_features_to_file(motifs, './data/roi_data/motifs_4.txt')

