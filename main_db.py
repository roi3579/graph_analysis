from utils.graph_wrapper import GraphWrapper
from utils.features_saver import FeatureSaver
import datetime
import random
import sys

args = sys.argv[1:]
# first argument db_connection_path
input_path = args[0]
# second argument ouput_path
oupput_folder = args[1]
# third argument number of samples edges
number_of_edges = args[2]

def read_bulk(cursor, snap_dir, snap, nodes_string):
    query = "select ud.InScanUserID,ud.AccountType from ljhistory.userdetails_"+snap+" ud where ud.InScanUserID in (%s)" % nodes_string
    print query

    cursor.execute(query)

    f = open(snap_dir + '\\accountstypes.txt', 'a')
    for (uid, account) in cursor:
        f.writelines(str(uid) + ' ' + str(account) + '\n')

    f.close()

    doi = ['summer'
        , 'the beatles'
        , 'cars'
        , 'traveling'
        , 'animals'
        , 'anime'
        , 'art'
        , 'books'
        , 'boys'
        , 'cars'
        , 'cats'
        , 'chocolate'
        , 'coffee'
        , 'computers'
        , 'concerts'
        , 'cooking'
        , 'dancing'
        , 'dogs'
        , 'drawing'
        , 'family'
        , 'fashion'
        , 'food'
        , 'friends'
        , 'girls'
        , 'guitar'
        , 'harry potter'
        , 'internet'
        , 'laughing'
        , 'love'
        , 'manga'
        , 'movies'
        , 'music'
        , 'painting'
        , 'photography'
        , 'pictures'
        , 'piercings'
        , 'poetry'
        , 'rain'
        , 'reading'
        , 'rock'
        , 'sex'
        , 'shopping'
        , 'singing'
        , 'sleeping'
        , 'snowboarding'
        , 'stars'
        , 'swimming'
        , 'taking back sunday'
        , 'tattoos'
        , 'video games'
        , 'writing']

    query = "select ui.UserID,i.InterestName from ljhistory.userinterests_" + snap + " ui join ljhistory.interests i on ui.UserID in (%s) " % nodes_string
    query = query + "and i.InterestName in (%s)" % ', '.join("'" + str(i) + "'" for i in doi)
    query = query + " and ui.InterestID = i.InterestID"

    cursor.execute(query)

    interest_to_vertex = {}
    for d in doi:
        interest_to_vertex[d] = []
    for (uid, interest_name) in cursor:
        print
        interest_to_vertex[str(interest_name)].append(str(uid))

    for interest in doi:
        f = open(snap_dir + '\\doi\\' + str(interest) + '.txt', 'a')
        for n in interest_to_vertex[interest]:
            f.writelines(str(n) + ' ' + '1\n')
        f.close()

print 'start graph', datetime.datetime.now()
graph_wrapper = GraphWrapper()
feature_saver = FeatureSaver()
#load the graph
graph_wrapper.load_from_db(is_directed=True, file_path=input_path)

# graph_wrapper = graph_wrapper.sample_uniform_from_edges(number_of_edges=number_of_edges)
graph_wrapper = graph_wrapper.sample_by_vertices_explore(number_of_start_vertices=15,explore_length=2)
print len(graph_wrapper.get_vertices_list())
random_vertices = graph_wrapper.get_max_connected_vertices(mode='WEAK')
print len(random_vertices)
degrees = graph_wrapper.degree(vertices_list=random_vertices)
count_edge = 0
for v in degrees:
    count_edge += degrees[v][0]


print 'edges:', count_edge
print 'vertices:', len(random_vertices)

# read_bulk()



# print 'start degrees',datetime.datetime.now()
# degrees= graph_wrapper.degree(vertices_list=random_vertices)
# print 'start write', datetime.datetime.now()
# feature_saver.save_vertex_features_to_file(degrees, oupput_folder + '/degrees.txt')
#
# print 'start kcore', datetime.datetime.now()
# kcore_features= graph_wrapper.k_coreness(vertices_list=random_vertices)
# print 'start write', datetime.datetime.now()
# feature_saver.save_vertex_features_to_file(kcore_features, oupput_folder + '/kcore.txt')
#
# print 'start page',datetime.datetime.now()
# pagerank_features= graph_wrapper.page_rank(vertices_list=random_vertices)
# print 'start write', datetime.datetime.now()
# feature_saver.save_vertex_features_to_file(pagerank_features, oupput_folder + '/page_rank.txt')
#
# print 'start closeness',datetime.datetime.now()
# closeness_features= graph_wrapper.closeness(vertices_list=random_vertices)
# print 'start write', datetime.datetime.now()
# feature_saver.save_vertex_features_to_file(closeness_features, oupput_folder + '/closeness.txt')
#
# print 'start betweenness',datetime.datetime.now()
# betweenness_features= graph_wrapper.betweenness(vertices_list=random_vertices)
# print 'start write', datetime.datetime.now()
# feature_saver.save_vertex_features_to_file(betweenness_features, oupput_folder + '/betweenness.txt')
#
# print 'start bfs moments',datetime.datetime.now()
# bfs_moments= graph_wrapper.bfs_moments(vertices_list=random_vertices)
# print 'start write', datetime.datetime.now()
# feature_saver.save_vertex_features_to_file(bfs_moments, oupput_folder + '/bfs_moments.txt')
#
# print 'start motif3',datetime.datetime.now()
# motifs_3= graph_wrapper.motif(vertices_list=random_vertices, motif_veriation_folder='./graph_algos/motifs_veriation',motif_size=3)
# print 'start write', datetime.datetime.now()
# feature_saver.save_vertex_features_to_file(motifs_3, oupput_folder + '/motifs3.txt')

# print 'start motif4',datetime.datetime.now()
# motifs_4= graph_wrapper.motif(vertices_list=random_vertices, motif_veriation_folder='./graph_algos/motifs_veriation',motif_size=4)
# print 'start write', datetime.datetime.now()
# feature_saver.save_vertex_features_to_file(motifs_4, oupput_folder + '/motifs4.txt')
# print 'done write', datetime.datetime.now()
