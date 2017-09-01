import os
doi_dir = '../data/directed/livejournal/snap0019/doi_750000/'

dois = os.listdir(doi_dir)
for doi in dois:
    count = 0
    total_count =0
    if doi == 'accountstypes.txt':
        continue
    with file(doi_dir+doi,'r') as f:
        for line in f:
            total_count += 1
            if ' 1' in line:
                count += 1
    print doi.replace('.txt','').replace(' ','_'), count