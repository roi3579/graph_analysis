from datetime import datetime
from utils.graph_wrapper import GraphWrapper
import sys

# input_path = r'./data/directed/livejournal/snap0001/input.json'
sample_size = int(sys.argv[1])
# sample_size = 500000

input_path = r'./data/directed/livejournal/snap0001/uniform_sample_p_{0}.txt'.format(sample_size)
print 'start graph: {0}'.format( datetime.now())
graph_wrapper = GraphWrapper()
graph_wrapper.load_from_file(is_directed=True, file_path=input_path)

# r_1 = 2
r_1 = int(sys.argv[2])
# r_2 = 8
r_2 = int(sys.argv[3])
for i in range(r_1,r_2):
    if i <10:
        snap = '000' + str(i)
    else:
        snap = '00' + str(i)

    input_path = r'./data/directed/livejournal/snap{0}/input.json'.format(snap)
    graph_wrapper2 = GraphWrapper()
    graph_wrapper2.load_from_db(is_directed=True, file_path=input_path)

    sub_g = graph_wrapper2.create_sub_graph(graph_wrapper.get_vertices_list())
    sub_g.save_graph_to_file('./data/directed/livejournal/snap{0}/uniform_sample_p_{1}.txt'.format(snap,sample_size))

