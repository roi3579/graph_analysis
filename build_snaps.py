from datetime import datetime
from utils.graph_wrapper import GraphWrapper

# input_path = r'./data/directed/livejournal/snap0001/input.json'
input_path = r'./data/directed/livejournal/snap0001/uniform_sample_p_500000.txt'
print 'start graph: {0}'.format( datetime.now())
graph_wrapper = GraphWrapper()
graph_wrapper.load_from_file(is_directed=True, file_path=input_path)


input_path = r'./data/directed/livejournal/snap0002/input.json'
graph_wrapper2 = GraphWrapper()
graph_wrapper2.load_from_db(is_directed=True, file_path=input_path)

sub_g = graph_wrapper2.create_sub_graph(graph_wrapper.get_vertices_list())
sub_g.save_graph_to_file('./data/directed/livejournal/snap0002/uniform_sample_p_500000.txt')

