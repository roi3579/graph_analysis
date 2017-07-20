from utils.graph_wrapper import GraphWrapper
from datetime import datetime
import random
import multiprocessing

def write_time(f,algo):
    print 'start {0} {1}'.format(algo,datetime.now())
    f.writelines('start {0} {1}\n'.format(algo,datetime.now()))
    f.flush()


def algos_single_smaple(graph_wrapper, vertices_list, number_of_random_vertices):
    with open('./data/directed/livejournal/snap0001/times_{0}.txt'.format(number_of_random_vertices), 'w') as f:
        write_time(f,str(number_of_random_vertices))
        random_vertices = random.sample(vertices_list, number_of_random_vertices)

        write_time(f,'degrees')
        degrees = graph_wrapper.degree(vertices_list=random_vertices)
        write_time(f,'kcore')
        kcore_features = graph_wrapper.k_coreness(vertices_list=random_vertices)
        write_time(f,'pagerank')
        pagerank_features = graph_wrapper.page_rank(vertices_list=random_vertices)
        write_time(f,'closeness')
        closeness_features = graph_wrapper.closeness(vertices_list=random_vertices)
        write_time(f,'betweenes')
        betweenness_features = graph_wrapper.betweenness(vertices_list=random_vertices)
        write_time(f,'bfs moments')
        bfs_moments = graph_wrapper.bfs_moments(vertices_list=random_vertices)
        write_time(f,'motifs 3')
        motifs_3 = graph_wrapper.motif(vertices_list=random_vertices,
                                       motif_veriation_folder='./graph_algos/motifs_veriation', motif_size=3)
        write_time(f,'done')
    f.close()

input_path = r'./data/directed/livejournal/snap0001/input.json'
numbers_of_random_vertices = [5000, 10000, 50000, 100000]
graph_wrapper = GraphWrapper()
graph_wrapper.load_from_db(is_directed=True,file_path=input_path)
vertices_list = graph_wrapper.get_vertices_list()
processes = []
for number_of_random_vertices in numbers_of_random_vertices:
    processes.append(multiprocessing.Process(target=algos_single_smaple, args=(graph_wrapper, vertices_list, number_of_random_vertices)))
    # algos_single_smaple(graph_wrapper, vertices_list, number_of_random_vertices)

for pr in processes:
    pr.start()

