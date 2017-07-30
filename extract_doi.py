# -*- coding: utf-8 -*-
import pymysql
import json
from utils.graph_wrapper import GraphWrapper
from datetime import datetime
import os
import sys


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]

def read_bulk(snap_dir, snap, vertices):

    file_path = r'./data/directed/livejournal/snap0001/input.json'
    with open(file_path, 'r') as f:
        db_paras = json.load(f)
    connection_params = db_paras['connection_details']
    cnx =  pymysql.connect(user=connection_params['user'],
                          password=connection_params['pass'],
                          host=connection_params['host'],
                          database=connection_params['database'])

    cursor = cnx.cursor()

    vertices_str = ','.join([str(v) for v in vertices])
    query = "select ud.InScanUserID,ud.AccountType from ljhistory.userdetails_{0} ud" \
            " where ud.InScanUserID in ({1})".format(snap,vertices_str)

    doi_directory = '{0}/doi_{1}/'.format(snap_dir,sample_size)
    if not os.path.exists(doi_directory):
        os.mkdir(doi_directory)

    cursor.execute(query)
    f = open(doi_directory + '/accountstypes.txt', 'a')
    for (uid, account) in cursor:
        f.writelines(str(uid) + ' ' + str(account) + '\n')
    f.close()

    doi_id_to_name_dict = {'13': 'музыка',
'18': 'internet',
'705': 'art',
'707': 'computers',
'709': 'movies',
'711': 'music',
'713': 'photography',
'1395': 'fashion',
'1397': 'guitar',
'1665': 'rock',
'2386': 'traveling',
'2769': 'reading',
'2774': 'video games',
'3032': 'fantasy',
'3046': 'rain',
'3051': 'sex',
'3054': 'tattoos',
'3568': 'books',
'3627': 'writing',
'3764': 'cats',
'5013': 'painting',
'5016': 'авто',
'5708': 'stars',
'5777': 'anime',
'6401': 'drawing',
'6403': 'poetry',
'6735': 'love',
'7163': 'concerts',
'7922': 'animals',
'8609': 'manga',
'9571': 'dogs',
'10693': 'dancing',
'11333': 'cooking',
'11339': 'food',
'12025': 'family',
'12480': 'boys',
'12765': 'shopping',
'13726': 'coffee',
'14764': 'acting',
'16300': 'friends',
'16844': 'laughing',
'16847': 'sleeping',
'16854': 'harry potter',
'18566': 'singing',
'25672': 'chocolate',
'25755': 'swimming',
'27299': 'cheese',
'39624': 'dvds',
'102829': 'piercings',
'443545': 'автомобили КИА'
}

    interest_ids = ','.join(doi_id_to_name_dict.keys())
    query = 'select ui.UserID, ui.InterestID from userinterests_{0} ui where' \
            ' ui.InterestID in ({1}) and ui.UserID in ({2})'.format(snap,interest_ids,vertices_str)

    cursor.execute(query)

    interest_to_vertex = {}

    for d_key in doi_id_to_name_dict.keys():
        interest_to_vertex[d_key] = []
    for (user_id, interest_id) in cursor:
        interest_to_vertex[str(interest_id)].append(str(user_id))

    for interest_id in doi_id_to_name_dict.keys():
        f = open('{0}/{1}.txt'.format(doi_directory,doi_id_to_name_dict[interest_id]), 'a')
        for n in interest_to_vertex[interest_id]:
            f.writelines(str(n) + ' ' + '1\n')
        f.close()


# sample_size = 500000
sample_size = int(sys.argv[1])

# chunks_size = 100000
chunks_size = int(sys.argv[2])

for snap_i in range(4,20):
    print snap_i
    if snap_i < 10:
        snap = '000'+str(snap_i)
    else:
        snap = '00'+str(snap_i)
    # snap = '0001'
    snap_dir = r'./data/directed/livejournal/snap{0}/'.format(snap)

    graph = GraphWrapper()
    graph.load_from_file(is_directed=True,file_path='./data/directed/livejournal/snap{0}/uniform_sample_p_{1}.txt'
                         .format(snap,sample_size))

    vertices = graph.get_vertices_list()
    vertices_chunks = list(chunks(vertices, chunks_size))
    number_of_chunks = len(vertices_chunks)
    for v in vertices_chunks:
        print datetime.now()
        print number_of_chunks
        number_of_chunks -=1
        read_bulk(snap_dir,snap,v)

