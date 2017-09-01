from scipy import stats
import os


def init_dict(file_path,separator,index):
    vertex_to_somthing ={}
    with file(file_path) as f:
        for line in f:
            words = line.split(separator)
            vertex = words[0]
            feature = float(words[index].replace('\n', ''))
            vertex_to_somthing[vertex] = feature
    return vertex_to_somthing

def print_feature_doi_correlation(feature_name,doi_name,doi_path, feature_path,i):

    vertex_to_feature = init_dict(feature_path, separator=',',index=i)
    vertex_to_tag = init_dict(doi_path, separator=' ',index=1)
    doi = []
    features = []
    for vertex in vertex_to_tag:
        doi.append(vertex_to_tag[vertex])
        features.append(vertex_to_feature[vertex])
    corr, pvalue = stats.spearmanr(doi, features)
    print '{0}_{1},{2},{3}'.format(feature_name, i-1, doi_name, corr)

base_dir = './../data/directed/livejournal/snap0001/'

# features = ['closeness', 'kcore', 'page_rank']
# features = ['motifs_3']
features = ['/propagation_750000_20/propagation']
dois = os.listdir(base_dir+'/doi_750000/')
dois = [d.replace('.txt','') for d in dois]

for feature in features:
    for i in range(1, 5):
        for doi in dois:
            print_feature_doi_correlation(doi, doi,
                doi_path=base_dir+'/doi_750000/{0}.txt'.format(doi),
                feature_path=base_dir+feature+'_{0}.txt'.format(doi), i=i)

