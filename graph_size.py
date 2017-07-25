from datetime import datetime
from utils.graph_wrapper import GraphWrapper
from utils.features_saver import FeatureSaver
import sys


def write_log(f,data):
    f.writelines(data+'\n')
    print data


def graph_sample_uniform_edges(graph_wrapper, sample_size):
    sub_g = graph_wrapper.sample_uniform_from_edges(number_of_edges=sample_size)
    vertices_list = sub_g.get_max_connected_vertices(mode='WEAK')
    degrees = sub_g.degree(vertices_list=vertices_list)
    count_edge = 0
    for v in degrees:
        count_edge += degrees[v][0]
    write_log('edges number: {0}'.format(count_edge))
    write_log('vertices number: {0}\n'.format(len(vertices_list)))


def graph_sample_explore_over_vertices(graph_wrapper, number_of_start_vertices, explore_length):
    write_log('start vertices: {0}'.format(number_of_start_vertices))
    write_log('length from start: {0}'.format(explore_length))
    sub_g = graph_wrapper.sample_by_vertices_explore(number_of_start_vertices=number_of_start_vertices,
                                                     explore_length=explore_length)
    write_log('total vertices: {0}'.format(len(sub_g.get_vertices_list())))
    random_vertices = sub_g.get_max_connected_vertices(mode='WEAK')
    write_log('max connected vertices: {0}'.format(len(random_vertices)))
    degrees = sub_g.degree(vertices_list=random_vertices)
    count_edge = 0
    for v in degrees:
        count_edge += degrees[v][0]
    write_log('edges: {0}'.format(count_edge))
    write_log('vertices: {0}\n'.format(len(random_vertices)))
    return sub_g


def graph_sample_uniform_vertices(f,graph_wrapper, number_of_vertices):
    sub_g = graph_wrapper.sample_uniform_by_vertices(number_of_vertices=number_of_vertices)
    write_log(f,'total vertices: {0}'.format(len(sub_g.get_vertices_list())))
    random_vertices = sub_g.get_max_connected_vertices(mode='WEAK')
    write_log(f,'max connected vertices: {0}'.format(len(random_vertices)))
    degrees = sub_g.degree(vertices_list=random_vertices)
    count_edge = 0
    for v in degrees:
        count_edge += degrees[v][0]
    write_log(f,'edges: {0}'.format(count_edge))
    write_log(f,'vertices: {0}\n'.format(len(random_vertices)))
    return sub_g

input_path = r'./data/directed/livejournal/snap0001/input.json'
print 'start graph: {0}'.format( datetime.now())
graph_wrapper = GraphWrapper()
graph_wrapper.load_from_db(is_directed=True, file_path=input_path)

# write_log('start uniform edes\n')
# samples_sizes = [10000,50000,100000,1000000,2000000,4000000,8000000,16000000,32000000,64000000]
# for s in samples_sizes:
#     write_log(str(datetime.now()))
#     write_log('sample_size: {0}'.format(s))
#     graph_sample_uniform(graph_wrapper,s)
#

samples_sizes = [500000,750000,1000000,1500000,2000000]
for i in samples_sizes:
    with open('sampling_times_{0}.txt'.format(i), 'w') as f:
        write_log(f,'start uniform vertices\n')
        write_log(f,str(datetime.now()))
        write_log(f,'sample_size: {0}'.format(i))
        sub_g = graph_sample_uniform_vertices(f,graph_wrapper, number_of_vertices=i)
        sub_g.save_graph_to_file('./data/directed/livejournal/snap0001/uniform_sample_p_{0}.txt'.format(i))
        write_log(f,str(datetime.now()))

# write_log('start explore vertices\n')
# for start_vertices in range(1,10):
#     for explore_length in range(1,3):
#         write_log(str(datetime.now()))
#         graph_sample_explore_over_vertices(graph_wrapper, start_vertices, explore_length=explore_length)
#         sub_g.save_graph_to_file('./data/directed/livejournal/snap0001/explore_sample_{0}_{1}.txt'.format(start_vertices,explore_length))
