'''
Created on Jun 5, 2016

@author: SongWang
'''

import sqlite3
import csv 
import numpy as np

def poiupdate(dbname, outfile, sqlfile):
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()

    cur.execute('''select CLASS_HIGH, CLASS_LOW, count(*) from POI group by CLASS_HIGH, CLASS_LOW''' )
    POI = {}
    POI["DISTRICT_HASH"] = []
#    print "POI number" ,len(POI)
    for row in cur.fetchall():
        CLASS_HIGH, CLASS_LOW, count = row
	POI["POI"+str(CLASS_HIGH)+"X"+str(CLASS_LOW)] = {}
        
    features =  POI.keys()
    features.remove("DISTRICT_HASH") # insert all the features
    print "features number" ,len(features)
    
    cur.execute('''select * from POI''' )
    for row in cur.fetchall():
	    DISTRICT_HASH, CLASS_HIGH, CLASS_LOW, NUM = row
	    POI["POI"+str(CLASS_HIGH)+"X"+str(CLASS_LOW)][DISTRICT_HASH] = NUM
	    if DISTRICT_HASH not in POI["DISTRICT_HASH"]:
                POI["DISTRICT_HASH"].append(DISTRICT_HASH)
#for k in features:  
#    print k,len(POI[k])    
        
         
#convert to list of list, filling 0.
    POItab = {}
    POItab["DISTRICT_HASH"] =  POI["DISTRICT_HASH"]   
    for k in features:
        POItab[k]=[]
            
    for dist in POItab["DISTRICT_HASH"]:
#   print dist
        for k in features:
#        print k
            try:
                value = POI[k][dist]
            #            print "value",value
                POItab[k].append (value)
            except KeyError:
                POItab[k].append (0)   
	    
    tolist=[]
    features.insert(0,"DISTRICT_HASH")
    print "number of features", len(features)

    for k in features:
        tolist.append(POItab[k])
#transpose: 
    tolist = np.array(tolist)
    tolist = tolist.T   
  
    header = features
    with open("POI_NEW.csv", "w") as savefile:
        writer = csv.writer(savefile,lineterminator="\n")
	writer.writerow(header)
	for r in tolist:
            writer.writerow(r) 

    with open ('POI_NEW.csv', 'r') as f:
        reader = csv.reader(f)
        columns = next(reader) 
#    print "columns",columns  ## column names
	query ='''
             DROP TABLE IF EXISTS POI_NEW;
             CREATE TABLE POI_NEW (
             DISTRICT_HASH TEXT PRIMARY KEY NOT NULL,
             '''
	for i in range(1,len(columns)-1):
            query = query + ''+ columns[i] +' INT NOT NULL,\n'
	query= query + ''+ columns[i+1] +' INT NOT NULL)' 
#    print query
	cur.executescript(query)
    
	print "insert data in the table"
	query = 'insert into POI_NEW({0}) values ({1})'
	query = query.format(','.join(columns), ','.join('?' * len(columns)))
	for data in reader:
            cur.execute(query, data)
       

    print 'reading poiupdate.sql'

    with open (sqlfile, 'rt') as f:
        jointables = f.read() 
#print jointables    
        cur.execute( jointables )
    
    print 'finish executing poiupdate.sql'

    with open(outfile, "wb") as csv_file:
        csv_writer = csv.writer(csv_file)
	csv_writer.writerow([i[0] for i in cur.description]) # write headers
	csv_writer.writerows(cur)         

    conn.commit()
    conn.close()


    
