import os
samples = [750000,1000000]
for sample in samples:
    print sample
    for i in range(2,20):
        print i
        if i < 10:
            snap = '000' + str(i)
        else:
            snap = '00' + str(i)
        dir = '../data/directed/livejournal/snap{0}/doi_{1}/'.format(snap, sample)
        vertices_file_path = '../data/directed/livejournal/snap{0}/uniform_sample_p_{1}.txt'.format(snap, sample)
        files_names = os.listdir(dir)
        for file_name in files_names:
            print file_name
            tags_file_path = dir + file_name
            output_path = '../data/directed/livejournal/snap{0}/doi_{1}/'.format(snap, sample)+file_name
            # tags_file_path = '../data/directed/livejournal/snap0001/doi_750000/music.txt'

            vertices_new_tags = {}
            with file(tags_file_path, 'r') as f:
                for line in f:
                    vertex, tag = line.split()
                    vertices_new_tags[vertex] = int(tag)

            with file(vertices_file_path, 'r') as f:
                for line in f:
                    src, trg, tag = line.split()
                    if src not in vertices_new_tags:
                        vertices_new_tags[src] = 0
                    if trg not in vertices_new_tags:
                        vertices_new_tags[trg] = 0

            with file(output_path, 'w') as f:
                for v in vertices_new_tags:
                    f.writelines('{0} {1}\n'.format(v, vertices_new_tags[v]))


