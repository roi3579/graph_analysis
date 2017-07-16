from utils.graph_wrapper import GraphWrapper
from utils.features_saver import FeatureSaver
import datetime
import random
import sys

args = sys.argv[1:]
#first argument db_connection_path
input_path = args[0]
#second argument ouput_path
oupput_folder = args[1]
#third argument number of random vertices
number_of_random_vertics = int(args[2])
print number_of_random_vertics

print 'start graph',datetime.datetime.now()
graph_wrapper = GraphWrapper()
feature_saver = FeatureSaver()
graph_wrapper.load_from_db(is_directed=True,file_path=input_path)
vertices_list = graph_wrapper.get_vertices_list()
random_vertices = random.sample(vertices_list,number_of_random_vertics)

print 'start degrees',datetime.datetime.now()
degrees= graph_wrapper.degree(vertices_list=random_vertices)
print 'start write', datetime.datetime.now()
feature_saver.save_vertex_features_to_file(degrees, oupput_folder + '/degrees.txt')

print 'start kcore', datetime.datetime.now()
kcore_features= graph_wrapper.k_coreness(vertices_list=random_vertices)
print 'start write', datetime.datetime.now()
feature_saver.save_vertex_features_to_file(kcore_features, oupput_folder + '/kcore.txt')

print 'start page',datetime.datetime.now()
pagerank_features= graph_wrapper.page_rank(vertices_list=random_vertices)
print 'start write', datetime.datetime.now()
feature_saver.save_vertex_features_to_file(pagerank_features, oupput_folder + '/page_rank.txt')

print 'start closeness',datetime.datetime.now()
closeness_features= graph_wrapper.closeness(vertices_list=random_vertices)
print 'start write', datetime.datetime.now()
feature_saver.save_vertex_features_to_file(closeness_features, oupput_folder + '/closeness.txt')

print 'start betweenness',datetime.datetime.now()
betweenness_features= graph_wrapper.betweenness(vertices_list=random_vertices)
print 'start write', datetime.datetime.now()
feature_saver.save_vertex_features_to_file(betweenness_features, oupput_folder + '/betweenness.txt')

print 'start bfs moments',datetime.datetime.now()
bfs_moments= graph_wrapper.bfs_moments(vertices_list=random_vertices)
print 'start write', datetime.datetime.now()
feature_saver.save_vertex_features_to_file(bfs_moments, oupput_folder + '/bfs_moments.txt')

print 'start motif3',datetime.datetime.now()
motifs_3= graph_wrapper.motif_3(vertices_list=random_vertices, motif_veriation_folder='./graph_algos/motifs_veriation')
print 'start write', datetime.datetime.now()
feature_saver.save_vertex_features_to_file(motifs_3, oupput_folder + '/motifs3.txt')
print 'done write', datetime.datetime.now()











