from datetime import datetime
from utils.graph_wrapper import GraphWrapper
from utils.features_saver import FeatureSaver


def graph_sample(sample_size):
    sub_g = graph_wrapper.sample_edges(number_of_edges=sample_size)
    vertices_list = sub_g.get_max_connected_vertices(mode='WEAK')
    degrees = sub_g.degree(vertices_list=vertices_list)
    count_edge = 0
    for v in degrees:
        count_edge += degrees[v][0]
    print 'edges number:',count_edge / 2
    print 'vertices number:',len(vertices_list)

input_path = r'./data/directed/livejournal/snap0001/input.json'
print 'start graph', datetime.now()
graph_wrapper = GraphWrapper()
feature_saver = FeatureSaver()
graph_wrapper.load_from_db(is_directed=True, file_path=input_path)
samples_sizes = [10000,50000,100000,1000000,2000000,4000000,8000000,16000000,32000000,64000000]
for s in samples_sizes:
    print 'sample_size:', s
    graph_sample(s)