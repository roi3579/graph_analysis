import json
import pymysql
import operator

file_path = r'./../data/directed/livejournal/snap0001/input.json'
with open(file_path, 'r') as f:
    db_paras = json.load(f)
connection_params = db_paras['connection_details']
cnx = pymysql.connect(user=connection_params['user'],
                      password=connection_params['pass'],
                      host=connection_params['host'],
                      database=connection_params['database'])

cursor = cnx.cursor()

print 'start'
query = 'SELECT InterestId FROM ljhistory.userinterests_0001 limit 5000'
cursor.execute(query)
doi_count = {}
for doi in cursor:
    if doi in doi_count:
        doi_count[doi] += 1
    else:
        doi_count[doi] = 1

# print doi_count
sorted_doi = sorted(doi_count.items(), key=operator.itemgetter(1),reverse=True)
with open('./../data/directed/livejournal/popular_doi.txt','w') as f:
    for doi in sorted_doi[0:2000]:
        f.writelines('{0},{1}\n'.format(doi[0][0],doi[1]))
print 'end'
