

def init_dict_by_file(file_path):
    vertex_to_tag = {}
    with file(file_path,'r') as f:
        for line in f:
            vertex, tag = line.replace('\n', '').split(' ')
            vertex_to_tag[vertex] = tag
    return vertex_to_tag


doi_file_path = './../data/directed/livejournal/snap0001/doi_750000/reading.txt'
vertex_to_tag_1 = init_dict_by_file(doi_file_path)

doi_file_path = './../data/directed/livejournal/snap0019/doi_750000/reading.txt'
vertex_to_tag_2 = init_dict_by_file(doi_file_path)


diff =[]
for vertex in vertex_to_tag_1:
    if vertex in vertex_to_tag_2:
        if vertex_to_tag_1[vertex] != vertex_to_tag_2[vertex]:
            print "'{0}',".format(vertex,vertex_to_tag_1[vertex],vertex_to_tag_2[vertex])
    else:
        diff.append(vertex)
print len(diff)